from django.db import models
from pages.models import Page


class HomePage(Page):
    """
    HomePage model that inherits from the base Page model.
    This allows creating homepage content from the admin panel.
    """
    # Additional fields specific to homepage
    hero_tagline = models.CharField(max_length=200, blank=True)
    hero_heading = models.CharField(max_length=200, blank=True)
    hero_description = models.TextField(blank=True)
    cta_primary_text = models.CharField(max_length=100, blank=True)
    cta_secondary_text = models.CharField(max_length=100, blank=True)
    
    # Stats
    happy_customers_value = models.CharField(max_length=20, blank=True)
    property_sales_value = models.CharField(max_length=20, blank=True)
    award_winning_value = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'

    def get_template(self):
        """Use the existing homepage template"""
        return "homepage/index.html"

    def serve(self, request):
        """Serve the homepage with additional context"""
        from django.shortcuts import render
        from .views import index
        # Use the existing index view for full homepage rendering
        return index(request)
