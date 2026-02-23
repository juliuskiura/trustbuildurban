from django.db import models
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel


class ProcessPage(Page):
    """
    ProcessPage model that inherits from the base Page model.
    This allows creating process page content from the admin panel.
    """

    class Meta:
        verbose_name = 'Process Page'
        verbose_name_plural = 'Process Pages'

    def get_template(self):
        return "process/process.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import process
        return process(request)


class HeaderSection(PageBase):
    """
    Process header section with OneToOne relationship to ProcessPage.
    Contains the eyebrow, heading, and description.
    """

    process_page = models.OneToOneField(
        "process.ProcessPage", on_delete=models.CASCADE, related_name="process_header"
    )

    # Section header
    eyebrow = models.CharField(max_length=100, blank=True, default="How We Work")
    heading = models.CharField(
        max_length=200, blank=True, default="The 7-Step TrustBuild Roadmap"
    )
    description = models.TextField(
        blank=True,
        default="Construction in Kenya doesn't have to be chaotic. We use a standardized corporate workflow to ensure predictable results every time.",
    )

    class Meta:
        verbose_name = "Process Header"
        verbose_name_plural = "Process Headers"

    def __str__(self):
        return f"Process Header for {self.process_page.title}"


class ProcessSteps(PageBase):
    """
    Process steps section with ForeignKey to ProcessPage.
    Contains quality gate info and step items.
    """

    process_page = models.ForeignKey(
        "process.ProcessPage",
        on_delete=models.CASCADE,
        related_name="process_steps_sections",
    )

    # Quality gate info
    quality_gate_label = models.CharField(
        max_length=100, blank=True, default="Quality Gate"
    )
    quality_gate_text = models.TextField(
        blank=True,
        default="This stage must be signed off by both our lead engineer and the client before proceeding.",
    )

    class Meta:
        verbose_name = "Process Steps Section"
        verbose_name_plural = "Process Steps Sections"

    def __str__(self):
        return f"Process Steps for {self.process_page.title}"


class ProcessStep(PageBase, OrderedModel):
    """
    Process step child model for ProcessSteps.
    Uses OrderedModel for ordering steps.
    """

    process_steps = models.ForeignKey(
        ProcessSteps, on_delete=models.CASCADE, related_name="steps"
    )

    # Step content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # Order
    order_with_respect_to = "process_steps"

    class Meta(OrderedModel.Meta):
        verbose_name = "Process Step"
        verbose_name_plural = "Process Steps"

    def __str__(self):
        return self.title


class ProcessCTA(PageBase):
    """
    Process CTA section with ForeignKey to ProcessPage.
    Contains the call-to-action heading and button.
    """

    process_page = models.ForeignKey(
        "process.ProcessPage",
        on_delete=models.CASCADE,
        related_name="process_cta_sections",
    )

    # CTA content
    heading = models.CharField(
        max_length=200, blank=True, default="Ready to take step one?"
    )
    button_text = models.CharField(
        max_length=100, blank=True, default="Book Initial Consultation"
    )
    button_link = models.CharField(max_length=200, blank=True, default="#contact")

    class Meta:
        verbose_name = "Process CTA"
        verbose_name_plural = "Process CTAs"

    def __str__(self):
        return f"Process CTA for {self.process_page.title}"
