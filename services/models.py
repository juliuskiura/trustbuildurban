from django.db import models
from pages.models import Page


class ServicePage(Page):
    """
    ServicePage model that inherits from the base Page model.
    This allows creating services page content from the admin panel.
    """
    # Additional fields specific to services page
    services_eyebrow = models.CharField(max_length=100, blank=True)
    services_heading = models.CharField(max_length=200, blank=True)
    services_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Service Page'
        verbose_name_plural = 'Service Pages'

    def get_template(self):
        return "services/services.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import services
        return services(request)
