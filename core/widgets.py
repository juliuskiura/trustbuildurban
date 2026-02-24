"""
Custom Django Admin Widgets with AI Content Generation.

This module provides custom form widgets with AI-assisted content generation.
"""

from django import forms


class AITextareaWidget(forms.Textarea):
    """
    A textarea widget with an AI content generation button.
    
    This widget adds a button next to the textarea that allows users to
    generate content using AI. The generated content is inserted into the textarea.
    """
    
    template_name = "core/widgets/ai_textarea.html"
    
    def __init__(
        self,
        attrs=None,
        ai_prompt: str = None,
        ai_context_fields: list = None,
        ai_button_text: str = "✨ Generate with AI",
        ai_loading_text: str = "Generating...",
    ):
        """
        Initialize the AI Textarea widget.
        
        Args:
            attrs: Standard widget attributes
            ai_prompt: Custom prompt for AI generation
            ai_context_fields: List of field names to use as context
            ai_button_text: Text for the AI generation button
            ai_loading_text: Text shown while generating
        """
        super().__init__(attrs)
        self.ai_prompt = ai_prompt
        self.ai_context_fields = ai_context_fields or []
        self.ai_button_text = ai_button_text
        self.ai_loading_text = ai_loading_text
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["ai_prompt"] = self.ai_prompt
        context["widget"]["ai_context_fields"] = self.ai_context_fields
        context["widget"]["ai_button_text"] = self.ai_button_text
        context["widget"]["ai_loading_text"] = self.ai_loading_text
        return context
    
    class Media:
        js = ["core/js/ai_content_generator.js"]
        css = {
            "all": ["core/css/ai_widget.css"]
        }


class AIHeroDescriptionWidget(AITextareaWidget):
    """
    Specialized AI widget for Hero Section description field.
    
    Pre-configured with appropriate prompts and context fields for
    generating hero section descriptions.
    """
    
    def __init__(self, attrs=None):
        super().__init__(
            attrs=attrs,
            ai_prompt="hero_description",
            ai_context_fields=["tagline", "heading_main", "company_name"],
            ai_button_text="✨ Generate Description",
            ai_loading_text="Generating description...",
        )
