"""
AI Content Generation Service for Django Admin.

This module provides AI-assisted content generation using OpenRouter API.
"""

import requests
import json
import os
from django.conf import settings


# Brand context for TrustBuildUrban
BRAND_CONTEXT = """You are a senior Brand Strategist and Construction Industry Marketing Expert.

You are writing content for a premium Kenyan Design & Build construction company that serves:

Kenyans living abroad (primary audience)

High-end and mid-market families in Kenya

The company:

Designs and builds custom residential homes

Builds on client-owned land

Assists with land search and acquisition

Manages projects from concept to completion

Provides structured reporting and stage-based payments

Offers virtual consultations for diaspora clients

Your goal is to position the company as:

A structured, transparent, and professionally managed building partner — not just a contractor.

Tone Requirements

The tone must be:

Professional

Calm

Clear

Structured

Trust-building

Premium but not flashy

Avoid hype, exaggerated claims, or aggressive marketing language.

Do NOT use words like:
"Cheapest", "Best", "Affordable luxury", "Limited offer".

Core Messaging Focus

Every piece of content must reinforce:

Transparent cost breakdown

Stage-based payment structure

Structured building process

Professional oversight

Quality workmanship

Remote project monitoring for diaspora clients

Clear documentation and contracts

The emotional outcome for the reader should be:

Confidence. Clarity. Peace of mind.

Writing Style Rules

Use short paragraphs

Use clear headings where appropriate

Be structured and logical

Avoid slang or casual phrases

Emphasize process and transparency"""


class AIContentGenerator:
    """
    A service class for generating content using OpenRouter AI API.
    """

    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = os.environ.get(
            "OPENROUTER_API_KEY",
            getattr(settings, "OPENROUTER_API_KEY", None)
        )
        self.model = getattr(settings, "OPENROUTER_MODEL", "z-ai/glm-4.5-air:free")
        self.brand_context = getattr(settings, "AI_BRAND_CONTEXT", BRAND_CONTEXT)

    def generate_content(
        self,
        prompt: str,
        context: dict = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        use_brand_context: bool = True,
    ) -> dict:
        """
        Generate content using the AI model.

        Args:
            prompt: The main instruction for content generation
            context: Dictionary with context fields (help_text, max_length, field_name, etc.)
            max_tokens: Maximum tokens in the response
            temperature: Creativity level (0-1)
            use_brand_context: Whether to include brand context

        Returns:
            dict with 'success', 'content', and 'error' keys
        """
        if not self.api_key:
            return {
                "success": False,
                "content": None,
                "error": "OpenRouter API key not configured. Set OPENROUTER_API_KEY in settings or environment."
            }

        # Build the message
        messages = []

        # System message with brand context
        if use_brand_context:
            system_message = self.brand_context
        else:
            system_message = (
                "You are a professional content writer. Write compelling, professional, "
                "and engaging content. Keep the content concise and impactful."
            )
        messages.append({"role": "system", "content": system_message})

        # Build user message with context
        user_message_parts = []

        # Add field context if provided
        if context:
            field_context = self._build_field_context(context)
            if field_context:
                user_message_parts.append(field_context)

        # Add the main prompt
        user_message_parts.append(f"Task: {prompt}")

        user_message = "\n\n".join(user_message_parts)
        messages.append({"role": "user", "content": user_message})

        try:
            response = requests.post(
                url=self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }),
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {
                    "success": True,
                    "content": content.strip(),
                    "error": None
                }
            else:
                error_msg = f"API Error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", error_msg)
                except:
                    pass
                return {
                    "success": False,
                    "content": None,
                    "error": error_msg
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "content": None,
                "error": "Request timed out. Please try again."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "content": None,
                "error": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "content": None,
                "error": f"Unexpected error: {str(e)}"
            }

    def _build_field_context(self, context: dict) -> str:
        """
        Build context string from field information.

        Args:
            context: Dictionary with field context

        Returns:
            Formatted context string
        """
        parts = []

        # Field name/label
        if context.get("field_label"):
            parts.append(f"Field: {context['field_label']}")

        # Help text - important for understanding what content is needed
        if context.get("help_text"):
            parts.append(f"Field Description: {context['help_text']}")

        # Max length constraint
        if context.get("max_length"):
            parts.append(f"Maximum Length: {context['max_length']} characters")

        # Field type
        if context.get("field_type"):
            parts.append(f"Field Type: {context['field_type']}")

        # Additional context values
        if context.get("related_values"):
            parts.append("Related Content:")
            for key, value in context["related_values"].items():
                if value:
                    parts.append(f"  - {key}: {value}")

        if parts:
            return "Context:\n" + "\n".join(parts)
        return ""

    def generate_field_content(
        self,
        field_label: str = None,
        help_text: str = None,
        max_length: int = None,
        field_type: str = None,
        custom_prompt: str = None,
        related_values: dict = None,
    ) -> dict:
        """
        Generate content for a specific field with full context.

        Args:
            field_label: The field's label/name
            help_text: The field's help text (important for understanding requirements)
            max_length: Maximum character length for the content
            field_type: Type of field (CharField, TextField, etc.)
            custom_prompt: User's custom prompt/instructions
            related_values: Dictionary of related field values for context

        Returns:
            dict with generation result
        """
        context = {
            "field_label": field_label,
            "help_text": help_text,
            "max_length": max_length,
            "field_type": field_type,
            "related_values": related_values or {},
        }

        # Build prompt based on available information
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt_parts = []

            if field_label:
                prompt_parts.append(f"Generate content for the '{field_label}' field.")

            if help_text:
                prompt_parts.append(f"The content should: {help_text}")

            if max_length:
                prompt_parts.append(f"Keep the content under {max_length} characters.")

            if field_type == "CharField":
                prompt_parts.append("Be concise - this is a short text field.")
            elif field_type == "TextField":
                prompt_parts.append("You can write a longer, more detailed response.")

            prompt_parts.append("\nGenerate appropriate content now.")
            prompt = "\n".join(prompt_parts)

        # Calculate appropriate max_tokens based on max_length
        if max_length:
            # Rough estimate: 1 token ≈ 4 characters
            max_tokens = min(max(100, max_length // 3), 1000)
        else:
            max_tokens = 500

        return self.generate_content(
            prompt=prompt,
            context=context,
            max_tokens=max_tokens,
            use_brand_context=True,
        )

    def generate_hero_description(
        self,
        tagline: str = None,
        heading_main: str = None,
        company_name: str = "TrustBuildUrban"
    ) -> dict:
        """
        Generate a hero section description.

        Args:
            tagline: The hero tagline for context
            heading_main: The main heading for context
            company_name: The company name

        Returns:
            dict with generation result
        """
        related_values = {}
        if tagline:
            related_values["Tagline"] = tagline
        if heading_main:
            related_values["Main Heading"] = heading_main
        related_values["Company"] = company_name

        return self.generate_field_content(
            field_label="Hero Description",
            help_text="A compelling description for the hero section that highlights expertise, emphasizes trust and quality, and encourages action",
            max_length=200,
            field_type="TextField",
            related_values=related_values,
        )


# Singleton instance
ai_generator = AIContentGenerator()
