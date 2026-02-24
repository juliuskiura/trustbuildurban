from django.db import models
from core.models import PageBase
from ordered_model.models import OrderedModel
from pages.models import ButtonStyle, Page


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
    Uses HomeHeroButton child model for dynamic button support.
    """

    homepage = models.OneToOneField(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="hero_section"
    )

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


class HomeHeroButton(PageBase, OrderedModel):
    """
    Button child model for HeroSection.
    Uses OrderedModel for ordering buttons within a hero section.
    """

    hero_section = models.ForeignKey(
        HeroSection, on_delete=models.CASCADE, related_name="buttons"
    )

    # Button content
    text = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=200, blank=True)
    icon = models.CharField(
        max_length=500, blank=True, help_text="SVG icon code or icon class"
    )

    # Button styling
    style = models.CharField(
        max_length=20, choices=ButtonStyle.choices, default=ButtonStyle.PRIMARY
    )
    size = models.CharField(
        max_length=20,
        choices=[
            ("small", "Small"),
            ("medium", "Medium"),
            ("large", "Large"),
        ],
        default="medium",
    )

    # Button behavior
    is_external = models.BooleanField(default=False, help_text="Open in new tab")
    is_full_width = models.BooleanField(default=False)

    # Order
    order_with_respect_to = "hero_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Hero Button"
        verbose_name_plural = "Hero Buttons"

    def __str__(self):
        return self.text or "Untitled Hero Button"


class ClientReview(PageBase):
    """
    Client review model with ForeignKey to HomePage.
    Contains rating, total reviews, and button information.
    Independent model (not related to StatsSection).
    """

    homepage = models.ForeignKey(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="client_reviews"
    )

    # Rating
    rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])

    # Total reviews
    total_reviews = models.CharField(max_length=20, blank=True, default="12,000+")

    # Label text
    label_text = models.CharField(max_length=100, blank=True, default="Client Reviews")

    # Button
    button_text = models.CharField(
        max_length=100, blank=True, default="Discover Excellence"
    )
    button_link = models.CharField(max_length=200, blank=True, default="#")

    class Meta:
        verbose_name = "Client Review"
        verbose_name_plural = "Client Reviews"

    def __str__(self):
        return f"Client Review ({self.rating} stars) - {self.total_reviews}"


# ============== Diaspora Section ==============


class DiasporaSection(PageBase):
    """
    Diaspora section model with ForeignKey to HomePage.
    Addresses challenges faced by diaspora builders in Kenya.
    """

    homepage = models.ForeignKey(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="diaspora_sections"
    )

    # Section content
    eyebrow = models.CharField(
        max_length=100,
        blank=True,
        default="The Diaspora Challenge",
    )
    heading = models.TextField(
        blank=True,
        default="Building in Kenya should not be a gamble.",
    )
    attribution = models.TextField(
        blank=True,
        default="TrustBuildUrban was founded to replace fear with structured, world-class building standards.",
    )

    # Featured project
    featured_label = models.CharField(
        max_length=100, blank=True, default="Featured Project"
    )
    featured_title = models.CharField(
        max_length=200, blank=True, default="The Grand Residence, Runda"
    )
    featured_image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diaspora_featured_images",
    )
    featured_image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name = "Diaspora Section"
        verbose_name_plural = "Diaspora Sections"

    def __str__(self):
        return f"Diaspora Section for {self.homepage.title}"


class DiasporaChallenge(PageBase, OrderedModel):
    """
    Challenge child model for DiasporaSection.
    Uses OrderedModel for ordering challenges.
    """

    diaspora_section = models.ForeignKey(
        DiasporaSection, on_delete=models.CASCADE, related_name="challenges"
    )

    # Challenge content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # Order
    order_with_respect_to = "diaspora_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Diaspora Challenge"
        verbose_name_plural = "Diaspora Challenges"

    def __str__(self):
        return self.title


# ============== Features Section ==============


class FeaturesSection(PageBase):
    """
    Features section model with ForeignKey to HomePage.
    Highlights why diaspora families trust TrustBuildUrban.
    """

    homepage = models.ForeignKey(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="features_sections"
    )

    # Section content
    eyebrow = models.CharField(
        max_length=100,
        blank=True,
        default="The TrustBuildUrban Standard",
    )
    heading = models.TextField(
        blank=True,
        default="Why Hundreds of Diaspora Families Trust Us",
    )

    class Meta:
        verbose_name = "Features Section"
        verbose_name_plural = "Features Sections"

    def __str__(self):
        return f"Features Section for {self.homepage.title}"


class Feature(PageBase, OrderedModel):
    """
    Feature child model for FeaturesSection.
    Uses OrderedModel for ordering features.
    """

    features_section = models.ForeignKey(
        FeaturesSection, on_delete=models.CASCADE, related_name="features"
    )

    # Feature content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    icon_path = models.TextField(blank=True, help_text="SVG icon code")

    # Order
    order_with_respect_to = "features_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def __str__(self):
        return self.title


# ============== Steps Section ==============


class StepsSection(PageBase):
    """
    Steps section model with ForeignKey to HomePage.
    Shows the 7-step architectural journey.
    """

    homepage = models.ForeignKey(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="steps_sections"
    )

    # Section content
    eyebrow = models.CharField(
        max_length=100,
        blank=True,
        default="Transparent Execution",
    )
    heading = models.TextField(
        blank=True,
        default="Our 7-Step Architectural Journey",
    )
    description = models.TextField(
        blank=True,
        default="A meticulously structured process from initial concept to the day we hand over your keys.",
    )

    class Meta:
        verbose_name = "Steps Section"
        verbose_name_plural = "Steps Sections"

    def __str__(self):
        return f"Steps Section for {self.homepage.title}"


class Step(PageBase, OrderedModel):
    """
    Step child model for StepsSection.
    Uses OrderedModel for ordering steps.
    """

    steps_section = models.ForeignKey(
        StepsSection, on_delete=models.CASCADE, related_name="steps"
    )

    # Step content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # Order
    order_with_respect_to = "steps_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Step"
        verbose_name_plural = "Steps"

    def __str__(self):
        return self.title


# ============== Services Section ==============


class ServicesSection(PageBase):
    """
    Services section model with ForeignKey to HomePage.
    Shows elite engineering and architectural services.
    """

    homepage = models.ForeignKey(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="services_sections"
    )

    # Section content
    subtitle = models.CharField(
        max_length=100,
        blank=True,
        default="Our Specializations",
    )
    heading = models.TextField(
        blank=True,
        default="Elite Engineering & Architectural Excellence",
    )

    class Meta:
        verbose_name = "Services Section"
        verbose_name_plural = "Services Sections"

    def __str__(self):
        return f"Services Section for {self.homepage.title}"


class Service(PageBase, OrderedModel):
    """
    Service child model for ServicesSection.
    Uses OrderedModel for ordering services.
    """

    services_section = models.ForeignKey(
        ServicesSection, on_delete=models.CASCADE, related_name="services"
    )

    # Service content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    icon = models.TextField(blank=True, help_text="SVG icon code")
    expertise = models.TextField(
        blank=True,
        help_text="Comma-separated list of expertise areas",
    )

    # Order
    order_with_respect_to = "services_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


# ============== Newsletter Section ==============


class NewsletterSection(PageBase):
    """
    Newsletter section model with ForeignKey to HomePage.
    Captures leads with diaspora home building guide.
    Uses NewsletterButton child model for CTA button.
    """

    homepage = models.ForeignKey(
        "homepage.HomePage",
        on_delete=models.CASCADE,
        related_name="newsletter_sections",
    )

    # Section content
    heading = models.TextField(
        blank=True,
        default="Free Diaspora Home Building Guide",
    )
    description = models.TextField(
        blank=True,
        default="Download our comprehensive manual on navigating land laws, approvals, and construction costs in Kenya from abroad.",
    )
    placeholder = models.CharField(
        max_length=100, blank=True, default="Enter your email"
    )

    class Meta:
        verbose_name = "Newsletter Section"
        verbose_name_plural = "Newsletter Sections"

    def __str__(self):
        return f"Newsletter Section for {self.homepage.title}"


class NewsletterButton(PageBase):
    """
    Button child model for NewsletterSection.
    """

    newsletter_section = models.ForeignKey(
        NewsletterSection, on_delete=models.CASCADE, related_name="buttons"
    )

    # Button content
    text = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=200, blank=True)
    icon = models.CharField(
        max_length=500, blank=True, help_text="SVG icon code or icon class"
    )

    # Button styling
    style = models.CharField(
        max_length=20, choices=ButtonStyle.choices, default=ButtonStyle.PRIMARY
    )
    size = models.CharField(
        max_length=20,
        choices=[
            ("small", "Small"),
            ("medium", "Medium"),
            ("large", "Large"),
        ],
        default="medium",
    )

    # Button behavior
    is_external = models.BooleanField(default=False, help_text="Open in new tab")
    is_full_width = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Newsletter Button"
        verbose_name_plural = "Newsletter Buttons"

    def __str__(self):
        return self.text or "Untitled Newsletter Button"


# ============== Who We Are Section ==============


class WhoWeAreSection(PageBase):
    """
    Who We Are section with background image.
    Full-width section with dark overlay and centered content.
    """

    homepage = models.OneToOneField(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="who_we_are_section"
    )

    # Section content
    label = models.CharField(
        max_length=100,
        blank=True,
        default="Who We Are",
    )
    heading = models.TextField(
        blank=True,
        default="Committed, client-focused, and process-driven builders.",
    )
    description = models.TextField(
        blank=True,
        default="We deliver world-class construction services with a focus on quality, transparency, and client satisfaction.",
    )

    # Button
    button_text = models.CharField(max_length=100, blank=True, default="Learn More")
    button_link = models.CharField(max_length=200, blank=True, default="/about")

    # Background image
    background_image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="who_we_are_sections",
    )
    background_image_url = models.URLField(max_length=500, blank=True)

    # Overlay
    overlay_opacity = models.IntegerField(
        default=40, help_text="Overlay opacity percentage (0-100)"
    )

    class Meta:
        verbose_name = "Who We Are Section"
        verbose_name_plural = "Who We Are Sections"

    def __str__(self):
        return f"Who We Are Section for {self.homepage.title}"


# ============== Stats Section ==============


class StatsSection(PageBase):
    """
    Stats section - 'By The Numbers' statistics.
    4-column grid for social proof.
    """

    homepage = models.OneToOneField(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="stats_section"
    )

    # Section content
    header = models.CharField(
        max_length=100,
        blank=True,
        default="TRUSTBUILD URBAN BY THE NUMBERS",
    )

    # Background pattern/image
    background_pattern = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stats_backgrounds",
    )

    class Meta:
        verbose_name = "Stats Section"
        verbose_name_plural = "Stats Sections"

    def __str__(self):
        return f"Stats Section for {self.homepage.title}"


class Stat(PageBase):
    """
    Statistic child model for StatsSection.
    """

    stats_section = models.ForeignKey(
        StatsSection, on_delete=models.CASCADE, related_name="stats"
    )

    # Stat content
    number = models.CharField(max_length=20, blank=True, default="500+")
    subtitle = models.CharField(
        max_length=100, blank=True, default="Projects Completed"
    )

    # Order for sorting
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = "Stat"
        verbose_name_plural = "Stats"
        ordering = ["order"]

    def __str__(self):
        return f"{self.number} - {self.subtitle}"


class PortFolioSection(PageBase):
    """
    Portfolio section model with ForeignKey to HomePage.
    Showcases completed projects with images and descriptions.
    """

    homepage = models.ForeignKey(
        "homepage.HomePage", on_delete=models.CASCADE, related_name="portfolio_sections"
    )

    # Section content
    eyebrow = models.CharField(
        max_length=100,
        blank=True,
        default="Our Work",
    )
    heading = models.TextField(
        blank=True,
        default="A Glimpse of Our Architectural Excellence",
    )
    description = models.TextField(
        blank=True,
        default="Luxury and family homes delivered across the country.",
    )
    button_text = models.CharField(max_length=100, blank=True, default="View Portfolio")
    button_link = models.CharField(max_length=200, blank=True, default="/portfolio")

    class Meta:
        verbose_name = "Portfolio Section"
        verbose_name_plural = "Portfolio Sections"

    def __str__(self):
        return f"Portfolio Section for {self.homepage.title}"
