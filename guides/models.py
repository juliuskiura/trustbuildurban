from django.db import models
from pages.models import Page


class GuidePage(Page):
    """
    GuidePage model that inherits from the base Page model.
    This allows creating guide page content from the admin panel.
    """
    # Additional fields specific to guide page
    guide_eyebrow = models.CharField(max_length=100, blank=True)
    guide_heading = models.CharField(max_length=200, blank=True)
    guide_description = models.TextField(blank=True)
    guide_image_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Guide Page'
        verbose_name_plural = 'Guide Pages'

    def get_template(self):
        return "guides/guide.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import guide
        return guide(request)
