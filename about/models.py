from django.db import models
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel


class AboutPage(Page):
    """
    AboutPage model that inherits from the base Page model.
    This allows creating about page content from the admin panel.
    """

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


class HeroSection(PageBase):
    """
    Hero section model with OneToOne relationship to AboutPage.
    Contains the company story, hero image, and quote.
    """

    about_page = models.OneToOneField(
        "about.AboutPage", on_delete=models.CASCADE, related_name="hero_section"
    )

    # Section header
    eyebrow = models.CharField(max_length=100, blank=True, default="Our Story")
    heading = models.CharField(
        max_length=200,
        blank=True,
        default="Excellence in Construction, Built on Trust.",
    )

    # Description
    description = models.TextField(
        blank=True,
        default="<p>Founded on the principle of radical transparency, TrustBuild Urban has become the premier choice for Kenyans living abroad and local high-end homeowners. We recognized a massive gap in the market: the lack of corporate accountability in residential construction. Our mission is to provide a seamless, stress-free building experience where quality is never compromised, and every shilling is accounted for. We don't just build houses; we build legacies.</p><p>Our mission is to provide a seamless, stress-free building experience where quality is never compromised, and every shilling is accounted for. We don't just build houses; we build legacies.</p>",
    )

    # Image - using ForeignKey to Image model
    image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="about_hero_sections",
    )
    image_url = models.URLField(max_length=500, blank=True)
    image_alt = models.CharField(
        max_length=200, blank=True, default="Architecture Team"
    )

    # Quote
    quote = models.TextField(
        blank=True, default="Transparency isn't a buzzword; it's our core architecture."
    )

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"Hero Section for {self.about_page.title}"


class Stat(PageBase, OrderedModel):
    """
    Stat model with ForeignKey to HeroSection.
    Uses OrderedModel for ordering stats.
    """

    hero_section = models.ForeignKey(
        HeroSection, on_delete=models.CASCADE, related_name="stats"
    )

    # Stat content
    value = models.CharField(max_length=20, blank=True)
    label = models.CharField(max_length=100, blank=True)

    # Order
    order_with_respect_to = "hero_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Stat"
        verbose_name_plural = "Stats"

    def __str__(self):
        return f"{self.value} - {self.label}"


class CorePillarsSection(PageBase):
    """
    Core Pillars section model with ForeignKey to AboutPage.
    Contains core values and standards.
    """

    about_page = models.ForeignKey(
        "about.AboutPage",
        on_delete=models.CASCADE,
        related_name="core_pillars_sections",
    )

    # Section header
    eyebrow = models.CharField(
        max_length=100, blank=True, default="The TrustBuild Standards"
    )
    heading = models.CharField(max_length=200, blank=True, default="Our Core Pillars")

    class Meta:
        verbose_name = "Core Pillars Section"
        verbose_name_plural = "Core Pillars Sections"

    def __str__(self):
        return f"Core Pillars Section for {self.about_page.title}"


class Pillar(PageBase, OrderedModel):
    """
    Pillar child model for CorePillarsSection.
    Uses OrderedModel for ordering pillars.
    """

    core_pillars_section = models.ForeignKey(
        CorePillarsSection, on_delete=models.CASCADE, related_name="pillars"
    )

    # Pillar content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    icon = models.TextField(blank=True, help_text="SVG icon code")

    # Order
    order_with_respect_to = "core_pillars_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Pillar"
        verbose_name_plural = "Pillars"

    def __str__(self):
        return self.title
