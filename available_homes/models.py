from django.db import models
from pages.models import Page


class AvailableHomesPage(Page):
    """
    AvailableHomesPage model that inherits from the base Page model.
    This allows creating available homes page content from the admin panel.
    """
    # Additional fields specific to available homes page
    hero_title = models.CharField(max_length=200, blank=True)
    hero_description = models.TextField(blank=True)
    cta_title = models.CharField(max_length=200, blank=True)
    cta_description = models.TextField(blank=True)
    cta_button_text = models.CharField(max_length=100, blank=True)
    cta_button_link = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Available Homes Page'
        verbose_name_plural = 'Available Homes Pages'

    def get_template(self):
        return "available_homes/available.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import available_homes
        return available_homes(request)
