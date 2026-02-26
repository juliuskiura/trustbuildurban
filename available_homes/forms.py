from django import forms
from .models import ShowingRequest, PropertyOffer


class ShowingRequestForm(forms.ModelForm):
    """
    Form for submitting property showing requests.
    """
    
    class Meta:
        model = ShowingRequest
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'preferred_date',
            'preferred_time',
            'is_first_time_buyer',
            'message',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'John',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'Doe',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'john@example.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': '+254 700 000000',
                'required': True,
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'type': 'date',
                'required': True,
            }),
            'preferred_time': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all',
            }),
            'is_first_time_buyer': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-accent rounded border-gray-300 focus:ring-accent',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'Any questions or special requests?',
                'rows': 3,
            }),
        }


class PropertyOfferForm(forms.ModelForm):
    """
    Form for submitting property offers.
    """
    
    class Meta:
        model = PropertyOffer
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'offer_amount',
            'financing_type',
            'is_first_time_buyer',
            'message',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'John',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'Doe',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'john@example.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': '+254 700 000000',
                'required': True,
            }),
            'offer_amount': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'e.g., KES 25,000,000',
                'required': True,
            }),
            'financing_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all',
            }),
            'is_first_time_buyer': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-accent rounded border-gray-300 focus:ring-accent',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder:text-gray-400',
                'placeholder': 'Any additional terms or questions?',
                'rows': 3,
            }),
        }
