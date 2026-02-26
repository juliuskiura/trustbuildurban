from django import forms
from .models import ContactSubmission, SubjectChoice


class ContactSubmissionForm(forms.ModelForm):
    """
    Form for the public contact page submission.
    Accepts a split first_name / last_name to match the template's fields.
    """

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "John",
            "class": (
                "w-full bg-white/50 border border-border rounded-xl px-6 py-4 "
                "focus:outline-none focus:border-accent transition-all text-sm"
            ),
        }),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Doe",
            "class": (
                "w-full bg-white/50 border border-border rounded-xl px-6 py-4 "
                "focus:outline-none focus:border-accent transition-all text-sm"
            ),
        }),
    )

    class Meta:
        model = ContactSubmission
        fields = ["first_name", "last_name", "email", "subject", "message"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "john@example.com",
                "class": (
                    "w-full bg-white/50 border border-border rounded-xl px-6 py-4 "
                    "focus:outline-none focus:border-accent transition-all text-sm"
                ),
            }),
            "subject": forms.Select(attrs={
                "class": (
                    "w-full bg-white/50 border border-border rounded-xl px-6 py-4 "
                    "focus:outline-none focus:border-accent transition-all text-sm"
                ),
            }),
            "message": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Tell us about your project…",
                "class": (
                    "w-full bg-white/50 border border-border rounded-xl px-6 py-4 "
                    "focus:outline-none focus:border-accent transition-all text-sm"
                ),
            }),
        }
