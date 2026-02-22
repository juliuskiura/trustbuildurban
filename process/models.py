from django.db import models
from pages.models import Page


class ProcessPage(Page):
    """
    ProcessPage model that inherits from the base Page model.
    This allows creating process page content from the admin panel.
    """
    # Additional fields specific to process page
    process_eyebrow = models.CharField(max_length=100, blank=True)
    process_heading = models.CharField(max_length=200, blank=True)
    process_description = models.TextField(blank=True)
    quality_gate_label = models.CharField(max_length=100, blank=True)
    quality_gate_text = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Process Page'
        verbose_name_plural = 'Process Pages'

    def get_template(self):
        return "process/process.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import process
        return process(request)
