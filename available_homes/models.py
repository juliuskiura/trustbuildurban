from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel


class AvailableHomesPage(Page):
    """
    AvailableHomesPage model that inherits from the base Page model.
    This allows creating available homes page content from the admin panel.
    """

    class Meta:
        verbose_name = 'Available Homes Page'
        verbose_name_plural = 'Available Homes Pages'

    def get_template(self):
        return "available_homes/available.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import available_homes
        return available_homes(request)


class AvailableHomesHeroSection(PageBase):
    """
    Hero section model with OneToOne relationship to AvailableHomesPage.
    Contains the title and description for the available homes page.
    """

    available_homes_page = models.OneToOneField(
        "available_homes.AvailableHomesPage",
        on_delete=models.CASCADE,
        related_name="hero_section",
    )

    # Hero content
    title = models.CharField(
        max_length=200,
        blank=True,
        default="Available Homes For Sale",
    )
    description = models.TextField(
        blank=True,
        default="High-quality homes built by TrustBuildUrban for immediate purchase. Move-in ready residences in Kenya's most sought-after neighborhoods.",
    )

    class Meta:
        verbose_name = "Available Homes Hero Section"
        verbose_name_plural = "Available Homes Hero Sections"

    def __str__(self):
        return f"Hero Section for {self.available_homes_page.title}"


class AvailableHome(PageBase, OrderedModel):
    """
    AvailableHome model for individual properties.
    Uses OrderedModel for ordering homes.
    Independent model not tied to a specific page.
    """

    # Status choices
    STATUS_CHOICES = [
        ("available", "Available"),
        ("under_offer", "Under Offer"),
        ("sold", "Sold"),
        ("reserved", "Reserved"),
    ]

    # Home content
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    price = models.CharField(
        max_length=100, blank=True, help_text="Price in KES format"
    )
    beds = models.PositiveIntegerField(default=0, blank=True)
    baths = models.PositiveIntegerField(default=0, blank=True)
    sqft = models.PositiveIntegerField(
        default=0, blank=True, help_text="Square footage"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True)
    description = models.TextField(
        blank=True, help_text="Detailed description of the property"
    )

    # Featured flag - if True, will be displayed prominently
    is_featured = models.BooleanField(default=False)

    class Meta(OrderedModel.Meta):
        verbose_name = "Available Home"
        verbose_name_plural = "Available Homes"

    def __str__(self):
        return self.title

    def get_status_display_custom(self):
        """Return a more readable status for display"""
        status_map = {
            "available": "Available",
            "under_offer": "Under Offer",
            "sold": "Sold",
            "reserved": "Reserved",
        }
        return status_map.get(self.status, self.status)

    def cover(self):
        """Get the cover image for this home."""
        return self.images.filter(is_cover=True).last()

    def get_image_url(self):
        """Return the primary image URL (cover image or first image)"""
        cover = self.cover()
        if cover:
            return cover.get_image_url()
        # Fallback to legacy image field
        if self.image:
            return self.image.image_url
        return self.image_url

    def get_absolute_url(self):
        return reverse("property_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BathroomInformation(models.Model):
    """
    BathroomInformation model for property bathroom information.
    """

    home = models.ForeignKey(
        AvailableHome, on_delete=models.CASCADE, related_name="bathroom_information"
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Bathroom Information"
        verbose_name_plural = "Bathroom Information"

    def __str__(self):
        return self.title


class BedroomInformation(models.Model):
    """
    BedroomInformation model for property bedroom information.
    """

    home = models.ForeignKey(
        AvailableHome, on_delete=models.CASCADE, related_name="bedroom_information"
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Bedroom Information"
        verbose_name_plural = "Bedroom Information"

    def __str__(self):
        return self.title


class HeatingAndCooling(models.Model):
    """
    HeatingAndCooling model for property heating and cooling information.
    """

    home = models.ForeignKey(
        AvailableHome,
        on_delete=models.CASCADE,
        related_name="heating_and_cooling",
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Heating and Cooling"
        verbose_name_plural = "Heating and Cooling"

    def __str__(self):
        return self.title


class KitchenAndDining(models.Model):
    """
    KitchenAndDining model for property kitchen and dining information.
    """

    home = models.ForeignKey(
        AvailableHome,
        on_delete=models.CASCADE,
        related_name="kitchen_and_dining",
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Kitchen and Dining"
        verbose_name_plural = "Kitchen and Dining"

    def __str__(self):
        return self.title


class InteriorFeatures(models.Model):
    """
    InteriorFeatures model for property interior features information.
    """

    home = models.ForeignKey(
        AvailableHome,
        on_delete=models.CASCADE,
        related_name="interior_features",
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Interior Features"
        verbose_name_plural = "Interior Features"

    def __str__(self):
        return self.title


class OtherRooms(models.Model):
    """
    OtherRooms model for property other rooms information.
    """

    home = models.ForeignKey(
        AvailableHome,
        on_delete=models.CASCADE,
        related_name="other_rooms",
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Other Rooms"
        verbose_name_plural = "Other Rooms"

    def __str__(self):
        return self.title


class GarageAndParking(models.Model):
    """
    GarageAndParking model for property garage and parking information.
    """

    home = models.ForeignKey(
        AvailableHome,
        on_delete=models.CASCADE,
        related_name="garage_and_parking",
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Garage and Parking"
        verbose_name_plural = "Garage and Parking"

    def __str__(self):
        return self.title


class UtilitiesAndGreenEnergy(models.Model):
    """
    UtilitiesAndGreenEnergy model for property utilities and green energy information.
    """

    home = models.ForeignKey(
        AvailableHome,
        on_delete=models.CASCADE,
        related_name="utilities_and_green_energy",
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Utilities and Green Energy"
        verbose_name_plural = "Utilities and Green Energy"

    def __str__(self):
        return self.title


class OutdoorSpaces(models.Model):
    """
    OutdoorSpaces model for property outdoor spaces information.
    """

    home = models.ForeignKey(
        AvailableHome,
        on_delete=models.CASCADE,
        related_name="outdoor_spaces",
    )
    title = models.CharField(max_length=200, blank=True)
    value = models.TextField(blank=True)

    order_with_respect_to = "home"

    class Meta:
        verbose_name = "Outdoor Spaces"
        verbose_name_plural = "Outdoor Spaces"

    def __str__(self):
        return self.title


class AvailableHomeImage(PageBase):
    """
    AvailableHomeImage model for property images.
    Allows multiple images per home with is_cover flag.
    """

    home = models.ForeignKey(
        AvailableHome, on_delete=models.CASCADE, related_name="images"
    )

    # Image - using ForeignKey to Image model
    image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="available_home_images",
    )  

    # Cover image flag
    is_cover = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Available Home Image"
        verbose_name_plural = "Available Home Images"

    def __str__(self):
        return f"Image for {self.home.title}"

    def get_image_url(self):
        """Return the image URL"""
        if self.image:
            return self.image.image_url
        return self.image_url


class AvailableHomesCTASection(PageBase):
    """
    CTA section model with OneToOne relationship to AvailableHomesPage.
    Contains the call-to-action for custom builds.
    """

    available_homes_page = models.OneToOneField(
        "available_homes.AvailableHomesPage",
        on_delete=models.CASCADE,
        related_name="cta_section",
    )

    # CTA content
    title = models.CharField(
        max_length=200,
        blank=True,
        default="Didn't find what you're looking for?",
    )
    description = models.TextField(
        blank=True,
        default="We can design and build a bespoke home specifically for you on your preferred piece of land.",
    )
    button_text = models.CharField(
        max_length=100,
        blank=True,
        default="LEARN ABOUT CUSTOM BUILD",
    )
    button_link = models.CharField(
        max_length=200,
        blank=True,
        default="/process/",
    )

    class Meta:
        verbose_name = "Available Homes CTA Section"
        verbose_name_plural = "Available Homes CTA Sections"

    def __str__(self):
        return f"CTA Section for {self.available_homes_page.title}"
