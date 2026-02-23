from django.db import models
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel


class ServicePage(Page):
    """
    ServicePage model that inherits from the base Page model.
    This allows creating services page content from the admin panel.
    """

    class Meta:
        verbose_name = 'Service Page'
        verbose_name_plural = 'Service Pages'

    def get_template(self):
        return "services/services.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import services
        return services(request)


class ServicesHeader(PageBase):
    """
    Services header section model with OneToOne relationship to ServicePage.
    Contains the eyebrow, heading, and description for the services page.
    """

    service_page = models.OneToOneField(
        "services.ServicePage", on_delete=models.CASCADE, related_name="header_section"
    )

    # Header content
    eyebrow = models.CharField(max_length=100, blank=True, default="What We Do")
    heading = models.CharField(
        max_length=200,
        blank=True,
        default="Specialized Solutions for Discerning Clients.",
    )
    description = models.TextField(
        blank=True,
        default="From the first site visit to the final coat of paint, we manage the complexities of construction so you don't have to.",
    )

    class Meta:
        verbose_name = "Services Header"
        verbose_name_plural = "Services Headers"

    def __str__(self):
        return f"Services Header for {self.service_page.title}"


class ServicesListSection(PageBase):
    """
    Services list section model with ForeignKey to ServicePage.
    Contains learn more text and service items.
    """

    service_page = models.ForeignKey(
        "services.ServicePage",
        on_delete=models.CASCADE,
        related_name="services_sections",
    )

    # Section content
    learn_more_text = models.CharField(max_length=100, blank=True, default="Learn More")

    class Meta:
        verbose_name = "Services List Section"
        verbose_name_plural = "Services List Sections"

    def __str__(self):
        return f"Services List for {self.service_page.title}"


class Service(PageBase, OrderedModel):
    """
    Service model for individual services.
    Uses OrderedModel for ordering services.
    """

    services_section = models.ForeignKey(
        ServicesListSection, on_delete=models.CASCADE, related_name="services"
    )

    # Service content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    icon = models.TextField(blank=True, help_text="SVG icon code")
    link = models.CharField(max_length=200, blank=True, default="/contact")

    # Image - using ForeignKey to Image model
    image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_images",
    )
    image_url = models.URLField(max_length=500, blank=True)

    # Order
    order_with_respect_to = "services_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title
