"""
Custom forms for Homepage app with AI-assisted content generation.
"""

from django import forms
from .models import HeroSection
from core.widgets import AIUniversalWidget, AIHeroDescriptionWidget, AITextFieldWidget


class HeroSectionForm(forms.ModelForm):
    """
    Custom form for HeroSection with AI-assisted description field.
    """

    class Meta:
        model = HeroSection
        fields = '__all__'
        widgets = {
            'description': AIHeroDescriptionWidget(
                attrs={
                    'rows': 4,
                    'cols': 80,
                    'placeholder': 'Enter a compelling description or use AI to generate one...'
                }
            ),
        }


class AIEnhancedModelForm(forms.ModelForm):
    """
    A base model form that automatically adds AI widgets to text fields.

    This form automatically extracts help_text and max_length from model fields
    and passes them to the AI widget for context-aware generation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Auto-enhance text fields with AI widgets
        self._enhance_text_fields()

    def _enhance_text_fields(self):
        """
        Automatically enhance TextField and CharField widgets with AI capabilities.
        """
        for field_name, field in self.fields.items():
            # Skip fields that already have AI widgets
            if hasattr(field.widget, "ai_field_label"):
                continue

            # Get field info from model if available
            model_field = None
            if hasattr(self._meta, "model") and self._meta.model:
                try:
                    model_field = self._meta.model._meta.get_field(field_name)
                except:
                    pass

            # Enhance TextField
            if isinstance(field, forms.CharField) and isinstance(
                field.widget, forms.Textarea
            ):
                help_text = model_field.help_text if model_field else field.help_text
                max_length = model_field.max_length if model_field else field.max_length
                label = field.label or field_name.replace("_", " ").title()

                field.widget = AITextFieldWidget(
                    attrs=field.widget.attrs,
                    help_text=help_text,
                    max_length=max_length,
                    label=label,
                    ai_allow_custom_prompt=True,
                )

            # Enhance CharField (text input)
            elif isinstance(field, forms.CharField) and isinstance(
                field.widget, forms.TextInput
            ):
                help_text = model_field.help_text if model_field else field.help_text
                max_length = model_field.max_length if model_field else field.max_length
                label = field.label or field_name.replace("_", " ").title()

                from core.widgets import AICharFieldWidget

                field.widget = AICharFieldWidget(
                    attrs=field.widget.attrs,
                    help_text=help_text,
                    max_length=max_length,
                    label=label,
                    ai_allow_custom_prompt=True,
                )
