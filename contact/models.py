from django.db import models
from pages.models import Page


class ContactPage(Page):
    """
    ContactPage model that inherits from the base Page model.
    This allows creating contact page content from the admin panel.
    """
    # Additional fields specific to contact page
    contact_eyebrow = models.CharField(max_length=100, blank=True)
    contact_heading = models.CharField(max_length=200, blank=True)
    contact_description = models.TextField(blank=True)
    
    # Contact info
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    map_image_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Contact Page'
        verbose_name_plural = 'Contact Pages'

    def get_template(self):
        """Use the existing contact template"""
        return "contact/contact.html"

    def serve(self, request):
        """Serve the contact page with additional context"""
        from django.shortcuts import render
        from .views import contact
        return contact(request)
