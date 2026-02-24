from django.db import models
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel


class PortfolioPage(Page):
    """
    PortfolioPage model that inherits from the base Page model.
    This allows creating portfolio page content from the admin panel.
    """

    class Meta:
        verbose_name = 'Portfolio Page'
        verbose_name_plural = 'Portfolio Pages'

    def get_template(self):
        return "portfolio/portfolio.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import portfolio
        return portfolio(request)


class PortfolioHeader(PageBase):
    """
    Portfolio header section model with OneToOne relationship to PortfolioPage.
    Contains the main heading and description for the portfolio page.
    """

    portfolio_page = models.OneToOneField(
        "portfolio.PortfolioPage",
        on_delete=models.CASCADE,
        related_name="header_section",
    )

    # Header content
    heading = models.CharField(max_length=200, blank=True, default="Our Portfolio")
    description = models.TextField(
        blank=True,
        default="A showcase of architectural brilliance and construction precision across Nairobi, Kiambu, and beyond.",
    )

    class Meta:
        verbose_name = "Portfolio Header"
        verbose_name_plural = "Portfolio Headers"

    def __str__(self):
        return f"Portfolio Header for {self.portfolio_page.title}"


class PortfolioProjectsSection(PageBase):
    """
    Portfolio projects section model with ForeignKey to PortfolioPage.
    Contains filters and project items.
    """

    portfolio_page = models.ForeignKey(
        "portfolio.PortfolioPage",
        on_delete=models.CASCADE,
        related_name="projects_sections",
    )

    # Section content
    learn_more_text = models.CharField(max_length=100, blank=True, default="Learn More")

    class Meta:
        verbose_name = "Portfolio Projects Section"
        verbose_name_plural = "Portfolio Projects Sections"

    def __str__(self):
        return f"Portfolio Projects for {self.portfolio_page.title}"


class PortfolioProjectCategory(PageBase,OrderedModel):
    """
    Portfolio project category model for project filtering.
    Uses OrderedModel for ordering categories.
    """

    # Category content
    name = models.CharField(max_length=50, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Portfolio Project Category"
        verbose_name_plural = "Portfolio Project Categories"

    def __str__(self):
        return self.name


class PortfolioProject(PageBase, OrderedModel):
    """
    Portfolio project model for individual projects.
    Uses OrderedModel for ordering projects.
    """

    # Status choices
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("planning", "Planning"),
        ("on_hold", "On Hold"),
    ]

    # Project content
    title = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True)
    description = models.TextField(blank=True)

    # Duration in months
    duration = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duration in months"
    )

    # Category for filtering - ForeignKey to PortfolioProjectCategory
    category = models.ForeignKey(
        PortfolioProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )

    # Highlight flag - if True, will be visible in homepage
    highlight_project = models.BooleanField(default=False)

    class Meta(OrderedModel.Meta):
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"

    def __str__(self):
        return self.title

    def cover(self):
        """Get the cover image for this project."""
        return self.images.filter(is_cover=True).last().img()

    


class ProjectImage(PageBase):
    """
    Project image model for portfolio projects.
    Allows multiple images per project with is_cover flag.
    """

    project = models.ForeignKey(
        PortfolioProject, on_delete=models.CASCADE, related_name="images"
    )

    # Image - using ForeignKey to Image model
    image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portfolio_project_images",
    )
    image_url = models.URLField(max_length=500,null=True, blank=True)

    # Cover image flag
    is_cover = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"Image for {self.project.title}"
    
    def img(self):
        """Return the cover image for this project."""
        return self.image.image if self.image else None