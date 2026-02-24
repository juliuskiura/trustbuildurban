"""
Custom Django Admin Widgets with AI Content Generation.

This module provides custom form widgets with AI-assisted content generation.
"""

from django import forms


class AIInputWidgetMixin:
    """
    Mixin that adds AI generation capabilities to any input widget.

    This mixin can be combined with any Django widget to add AI generation functionality.
    """

    def __init__(
        self,
        attrs=None,
        ai_field_label: str = None,
        ai_help_text: str = None,
        ai_max_length: int = None,
        ai_field_type: str = None,
        ai_context_fields: list = None,
        ai_button_text: str = "✨ Generate with AI",
        ai_loading_text: str = "Generating...",
        ai_allow_custom_prompt: bool = True,
        **kwargs
    ):
        """
        Initialize the AI widget mixin.

        Args:
            attrs: Standard widget attributes
            ai_field_label: Label for the field (used in AI prompt)
            ai_help_text: Help text describing what content is needed
            ai_max_length: Maximum character length for generated content
            ai_field_type: Type of field (CharField, TextField, etc.)
            ai_context_fields: List of field names to use as additional context
            ai_button_text: Text for the AI generation button
            ai_loading_text: Text shown while generating
            ai_allow_custom_prompt: Whether to allow user to enter custom prompts
        """
        super().__init__(attrs, **kwargs)
        self.ai_field_label = ai_field_label
        self.ai_help_text = ai_help_text
        self.ai_max_length = ai_max_length
        self.ai_field_type = ai_field_type
        self.ai_context_fields = ai_context_fields or []
        self.ai_button_text = ai_button_text
        self.ai_loading_text = ai_loading_text
        self.ai_allow_custom_prompt = ai_allow_custom_prompt

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["ai_field_label"] = (
            self.ai_field_label or name.replace("_", " ").title()
        )
        context["widget"]["ai_help_text"] = self.ai_help_text or ""
        context["widget"]["ai_max_length"] = self.ai_max_length or ""
        context["widget"]["ai_field_type"] = self.ai_field_type or "TextField"
        context["widget"]["ai_context_fields"] = ",".join(self.ai_context_fields)
        context["widget"]["ai_button_text"] = self.ai_button_text
        context["widget"]["ai_loading_text"] = self.ai_loading_text
        context["widget"]["ai_allow_custom_prompt"] = self.ai_allow_custom_prompt
        return context

    class Media:
        js = ["core/js/ai_content_generator.js"]
        css = {
            "all": ["core/css/ai_widget.css"]
        }


class AITextInputWidget(AIInputWidgetMixin, forms.TextInput):
    """
    Text input widget with AI content generation.

    Use this for CharField fields that need AI generation.
    """

    template_name = "core/widgets/ai_input.html"

    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs, ai_field_type="CharField", **kwargs)


class AITextareaWidget(AIInputWidgetMixin, forms.Textarea):
    """
    Textarea widget with AI content generation.

    Use this for TextField fields that need AI generation.
    """

    template_name = "core/widgets/ai_textarea.html"

    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs, ai_field_type="TextField", **kwargs)


class AIUniversalWidget(AIInputWidgetMixin, forms.Textarea):
    """
    Universal AI widget that adapts to any field type.

    This widget automatically detects field information from the form field
    and provides context-aware AI generation.
    """

    template_name = "core/widgets/ai_universal.html"

    def __init__(self, attrs=None, **kwargs):
        # Set defaults for universal use
        kwargs.setdefault("ai_allow_custom_prompt", True)
        super().__init__(attrs, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Try to extract field info from attrs if not explicitly set
        if not self.ai_max_length and attrs and "maxlength" in attrs:
            context["widget"]["ai_max_length"] = attrs["maxlength"]

        return context


# Convenience widgets for specific use cases

class AIHeroDescriptionWidget(AITextareaWidget):
    """
    Specialized AI widget for Hero Section description field.
    
    Pre-configured with appropriate prompts and context fields for
    generating hero section descriptions.
    """

    def __init__(self, attrs=None):
        super().__init__(
            attrs=attrs,
            ai_field_label="Hero Description",
            ai_help_text="A compelling description for the hero section that highlights expertise, emphasizes trust and quality, and encourages action",
            ai_max_length=200,
            ai_context_fields=["tagline", "heading_main", "company_name"],
            ai_button_text="✨ Generate Description",
            ai_loading_text="Generating description...",
        )


class AICharFieldWidget(AITextInputWidget):
    """
    AI widget optimized for short text fields (CharField).

    Includes character limit awareness and concise generation.
    """

    def __init__(
        self, attrs=None, max_length=None, help_text=None, label=None, **kwargs
    ):
        super().__init__(
            attrs=attrs,
            ai_field_label=label,
            ai_help_text=help_text,
            ai_max_length=max_length,
            ai_button_text="✨ Generate",
            ai_loading_text="Generating...",
            **kwargs
        )


class AITextFieldWidget(AITextareaWidget):
    """
    AI widget optimized for long text fields (TextField).

    Allows for longer, more detailed content generation.
    """

    def __init__(self, attrs=None, help_text=None, label=None, **kwargs):
        super().__init__(
            attrs=attrs,
            ai_field_label=label,
            ai_help_text=help_text,
            ai_button_text="✨ Generate Content",
            ai_loading_text="Generating content...",
            **kwargs
        )
