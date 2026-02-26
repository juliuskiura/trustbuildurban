from django.db import models
from pages.models import Page
from core.models import PageBase


class SubjectChoice(models.TextChoices):
    NEW_PROJECT = "new_project", "New Project Inquiry"
    DIASPORA = "diaspora", "Diaspora Consultation"
    PARTNERSHIP = "partnership", "Partnership Proposal"
    OTHER = "other", "Other"


class ContactPage(Page):
    """
    ContactPage model that inherits from the base Page model.
    This allows creating contact page content from the admin panel.
    """

    class Meta:
        verbose_name = 'Contact Page'
        verbose_name_plural = 'Contact Pages'

    def get_template(self):
        return "contact/contact.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import contact
        return contact(request)


class ContactHeader(PageBase):
    """
    Contact header section model with OneToOne relationship to ContactPage.
    Contains the eyebrow, heading, and description for the contact page.
    """

    contact_page = models.OneToOneField(
        "contact.ContactPage", on_delete=models.CASCADE, related_name="header_section"
    )

    # Header content
    eyebrow = models.CharField(max_length=100, blank=True, default="Get In Touch")
    heading = models.CharField(
        max_length=200, 
        blank=True, 
        default="Let's Build Your Legacy Together."
    )
    description = models.TextField(
        blank=True,
        default="Whether you're in the diaspora or local, we're here to provide the radical transparency and excellence your project deserves."
    )

    class Meta:
        verbose_name = "Contact Header"
        verbose_name_plural = "Contact Headers"

    def __str__(self):
        return f"Contact Header for {self.contact_page.title}"


class ContactContentSection(PageBase):
    """
    Contact content section model with OneToOne relationship to ContactPage.
    Contains form labels and contact information.
    """

    contact_page = models.OneToOneField(
        "contact.ContactPage", on_delete=models.CASCADE, related_name="content_section"
    )
    heading = models.CharField(max_length=200, blank=True, default="Contact Information")



class ContactSubmission(models.Model):
    """
    Model to store contact form submissions.
    """

    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    # Subject
    subject = models.CharField(max_length=50, choices=SubjectChoice.choices)

    # Message
    message = models.TextField()

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
