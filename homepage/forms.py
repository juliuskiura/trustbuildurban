"""
Custom forms for Homepage app with AI-assisted content generation.
"""

from django import forms
from .models import HeroSection
from core.widgets import AIHeroDescriptionWidget


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
