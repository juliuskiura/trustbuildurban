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

    # Form content
class ContactInfo(models.Model):
    section = models.ForeignKey(ContactContentSection, on_delete=models.CASCADE, related_name="contact_info_items")
    # Contact info fields directly on section
    label = models.CharField(
        max_length=100, blank=True, default="+254 712 345 678"
    )
    value = models.CharField(
        max_length=100, blank=True, default="info@trustbuildurban.co.ke"
    )
    icon= models.TextField()

    # Google Map
    map_embed_url = models.URLField(
        max_length=500,
        blank=True,
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.808!2d36.8219!3d-1.2921!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMsKwMTcnMjAuMCJTIDM2wrA0OScxMS4wIkU!5e0!3m2!1sen!2ske!4v1234567890",
    )
    map_label = models.CharField(max_length=100, blank=True, default="Office Location")

    class Meta:
        verbose_name = "Contact Content Section"
        verbose_name_plural = "Contact Content Sections"

    def __str__(self):
        return f"Contact Content for {self.contact_page.title}"


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
