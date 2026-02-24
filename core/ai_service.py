"""
AI Content Generation Service for Django Admin.

This module provides AI-assisted content generation using OpenRouter API.
"""

import requests
import json
import os
from django.conf import settings


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

    def generate_content(
        self,
        prompt: str,
        context: str = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> dict:
        """
        Generate content using the AI model.

        Args:
            prompt: The main instruction for content generation
            context: Additional context to help guide generation
            max_tokens: Maximum tokens in the response
            temperature: Creativity level (0-1)

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
        
        system_message = (
            "You are a professional content writer for a construction and real estate company "
            "called TrustBuildUrban. Write compelling, professional, and engaging content "
            "that resonates with diaspora clients looking to build homes in Kenya. "
            "Keep the content concise, impactful, and action-oriented."
        )
        messages.append({"role": "system", "content": system_message})

        # Add context if provided
        if context:
            user_message = f"Context: {context}\n\nTask: {prompt}"
        else:
            user_message = prompt

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
        context_parts = []
        if tagline:
            context_parts.append(f"Tagline: {tagline}")
        if heading_main:
            context_parts.append(f"Main Heading: {heading_main}")
        context_parts.append(f"Company: {company_name}")
        
        context = "\n".join(context_parts)

        prompt = (
            "Write a compelling hero section description (2-3 sentences) that:\n"
            "1. Highlights the company's expertise in construction for diaspora clients\n"
            "2. Emphasizes trust, quality, and transparency\n"
            "3. Encourages visitors to take action\n"
            "Keep it under 200 characters for impact."
        )

        return self.generate_content(prompt=prompt, context=context, max_tokens=150)


# Singleton instance
ai_generator = AIContentGenerator()
