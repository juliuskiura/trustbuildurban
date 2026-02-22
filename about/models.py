from django.db import models
from pages.models import Page


class AboutPage(Page):
    """
    AboutPage model that inherits from the base Page model.
    This allows creating about page content from the admin panel.
    """
    # Additional fields specific to about page
    story_eyebrow = models.CharField(max_length=100, blank=True)
    story_heading = models.CharField(max_length=200, blank=True)
    story_description_1 = models.TextField(blank=True)
    story_description_2 = models.TextField(blank=True)
    story_image_url = models.URLField(blank=True)
    story_quote = models.TextField(blank=True)
    
    # Stats
    years_experience_value = models.CharField(max_length=20, blank=True)
    projects_completed_value = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Pages'

    def get_template(self):
        """Use the existing about template"""
        return "about/about.html"

    def serve(self, request):
        """Serve the about page with additional context"""
        from django.shortcuts import render
        from .views import about
        return about(request)
