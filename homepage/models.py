from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from pages.models import Page, Button
from core.models import PageBase
from ordered_model.models import OrderedModel

class HomePage(Page):
    """
    HomePage model that inherits from the base Page model.
    This allows creating homepage content from the admin panel.
    """
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


class HeroSection(PageBase):
    """
    Hero section model with one-to-one relationship to HomePage.
    Uses generic Button model for dynamic button support.
    """

    homepage = models.OneToOneField(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="hero_section"
    )

    # Generic relation to buttons - allows unlimited buttons
    buttons = GenericRelation(Button, related_query_name="hero_sections")

    # Hero content
    tagline = models.CharField(max_length=200, blank=True)
    heading_main = models.CharField(max_length=200, blank=True)
    heading_highlight = models.CharField(max_length=100, blank=True)
    heading_suffix = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    # Background image - using ForeignKey to Image model
    background_image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hero_sections",
    )

    # Overlay settings
    overlay_opacity = models.IntegerField(
        default=50, help_text="Overlay opacity percentage (0-100)"
    )

    # Verified badge
    show_verified_badge = models.BooleanField(default=True)
    verified_text = models.CharField(max_length=50, default="Verified")

    # Live tracking
    show_live_tracking = models.BooleanField(default=True)
    live_tracking_text = models.CharField(
        max_length=100, default="Live Project Tracking"
    )

    # Company info
    company_name = models.CharField(max_length=100, blank=True)
    company_location = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"Hero Section for {self.homepage.title}"


class Stats(PageBase, OrderedModel):
    """
    Stats model with ForeignKey to HeroSection.
    Allows multiple stat items per hero section.
    """

    hero_section = models.ForeignKey(
        HeroSection, on_delete=models.CASCADE, related_name="stats"
    )

    # Stat content
    value = models.CharField(max_length=20, blank=True)
    label = models.CharField(max_length=100, blank=True)
    order_with_respect_to = 'hero_section'

    # Order

    class Meta(OrderedModel.Meta):
        verbose_name = "Stat"
        verbose_name_plural = "Stats"

    def __str__(self):
        return f"{self.value} - {self.label}"
