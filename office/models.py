import urllib.parse

from django.db import models
from django.conf import settings


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

class Company(models.Model):
    """
    Singleton-style model that stores all core company information.
    Legal details, contact data, social links, and registration numbers
    all live here. Only one record is expected (the company itself),
    but the model is not strictly enforced as a singleton so that
    staging / test data can co-exist.
    """

    # ── Identity ──────────────────────────────────────────────────────────
    name = models.CharField(
        max_length=200,
        help_text="Full legal name of the company.",
    )
    trading_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Brand / trading name if different from legal name (e.g. TrustBuild Urban).",
    )
    tagline = models.CharField(max_length=300, blank=True)

    # ── Legal / Registration ──────────────────────────────────────────────
    registration_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Company registration number (e.g. Kenya Companies Registry).",
    )
    tax_identification_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="KRA PIN / Tax ID.",
    )
    vat_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="VAT registration number if applicable.",
    )
    year_founded = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Year the company was incorporated.",
    )
    company_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Limited Liability Company, Partnership, Sole Proprietorship.",
    )
    country_of_incorporation = models.CharField(
        max_length=100,
        blank=True,
        default="Kenya",
    )

    # ── Physical Address ──────────────────────────────────────────────────
    physical_address = models.TextField(
        blank=True,
        help_text="Full street / building address.",
    )
    city = models.CharField(max_length=100, blank=True, default="Nairobi")
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default="Kenya")
    postal_code = models.CharField(max_length=20, blank=True)
    po_box = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="P.O. Box",
        help_text="e.g. P.O. Box 12345-00100, Nairobi",
    )

    # GPS pin for office/HQ
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Office/HQ latitude (right-click on Google Maps → copy coordinates).",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    # ── Contact ───────────────────────────────────────────────────────────
    primary_phone = models.CharField(max_length=30, blank=True)
    secondary_phone = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    primary_email = models.EmailField(blank=True)
    support_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # ── Social Media ──────────────────────────────────────────────────────
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter / X")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube")
    tiktok_url = models.URLField(blank=True, verbose_name="TikTok")

    # ── Timestamps ────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"

    def __str__(self):
        return self.trading_name or self.name

    @property
    def osm_embed_url(self):
        """OpenStreetMap iframe src for the office/HQ location."""
        if self.latitude and self.longitude:
            lat = float(self.latitude)
            lon = float(self.longitude)
            delta = 0.008  # ~900 m bounding box
            bbox = f"{lon - delta},{lat - delta},{lon + delta},{lat + delta}"
            return (
                f"https://www.openstreetmap.org/export/embed.html"
                f"?bbox={bbox}&layer=mapnik&marker={lat},{lon}"
            )
        # Fallback: text search using city + country
        location_text = ", ".join(filter(None, [self.city, self.country]))
        if location_text:
            q = urllib.parse.quote(location_text)
            return f"https://www.openstreetmap.org/export/embed.html?mlat=0&mlon=0#map=14/0/0&query={q}"
        return ""

    @property
    def osm_full_url(self):
        """OpenStreetMap link for 'View larger map'."""
        if self.latitude and self.longitude:
            return (
                f"https://www.openstreetmap.org/?mlat={self.latitude}"
                f"&mlon={self.longitude}#map=16/{self.latitude}/{self.longitude}"
            )
        location_text = ", ".join(filter(None, [self.city, self.country]))
        if location_text:
            q = urllib.parse.quote(location_text)
            return f"https://www.openstreetmap.org/search?query={q}"
        return "https://www.openstreetmap.org/"


# ---------------------------------------------------------------------------
# Company Images (logos, brand assets, office photos)
# ---------------------------------------------------------------------------

class CompanyImage(models.Model):
    """
    Images associated with the company — logos, brand assets, office
    photos, accreditation badges, etc.

    All image data is stored via a FK to `images.Image` so the
    existing image-management infrastructure (alt text, dimensions,
    usage tracking) is reused automatically.
    """

    IMAGE_TYPE_CHOICES = [
        ("logo_primary", "Primary Logo"),
        ("logo_secondary", "Secondary / Alternative Logo"),
        ("logo_white", "White / Reversed Logo"),
        ("logo_dark", "Dark Logo"),
        ("favicon", "Favicon"),
        ("office_photo", "Office Photo"),
        ("team_photo", "Team Photo"),
        ("accreditation", "Accreditation / Certificate Badge"),
        ("award", "Award"),
        ("other", "Other"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_images",
        help_text="Select from the shared Image library.",
    )
    image_type = models.CharField(
        max_length=30,
        choices=IMAGE_TYPE_CHOICES,
        default="other",
    )
    label = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short label or note (e.g. 'Light background variant').",
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Mark this as the default image for its type.",
    )
    order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Company Image"
        verbose_name_plural = "Company Images"
        ordering = ["image_type", "order"]

    def __str__(self):
        return f"{self.company} — {self.get_image_type_display()}"

    @property
    def image_url(self):
        if self.image:
            return self.image.image_url
        return ""


# ---------------------------------------------------------------------------
# Contact Person
# ---------------------------------------------------------------------------

class ContactPerson(models.Model):
    """
    A named contact (director, department head, sales agent, etc.)
    associated with the company.

    `user` is a nullable FK to `accounts.UserAccount`.  When set, the
    display name and email can be pulled from the linked account; when
    left blank the standalone fields are used instead (useful for
    external contacts or people who don't have a portal login).
    """

    ROLE_CHOICES = [
        ("ceo", "CEO / Managing Director"),
        ("coo", "COO / Operations Director"),
        ("cfo", "CFO / Finance Director"),
        ("sales", "Sales & Marketing"),
        ("legal", "Legal & Compliance"),
        ("customer_service", "Customer Service"),
        ("technical", "Technical / Engineering"),
        ("admin", "Administration"),
        ("other", "Other"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contact_persons",
    )

    # Optionally link to a portal user account
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_contact_roles",
        help_text=(
            "Link to a UserAccount. When set, the person's name and email "
            "are inherited from that account."
        ),
    )

    # Standalone identity fields (used when no user account is linked)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="other",
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Job title as displayed publicly (e.g. 'Head of Sales').",
    )

    # Portrait — reuses the shared Image library
    portrait = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_person_portraits",
        help_text="Profile photo from the shared Image library.",
    )

    bio = models.TextField(blank=True)
    is_public = models.BooleanField(
        default=True,
        help_text="Show this person on the public-facing website.",
    )
    order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Person"
        verbose_name_plural = "Contact Persons"
        ordering = ["order", "role"]

    # ── Helpers ───────────────────────────────────────────────────────────

    def get_full_name(self):
        """Return display name, preferring the linked user account."""
        if self.user:
            name = f"{self.user.first_name or ''} {self.user.last_name or ''}".strip()
            if name:
                return name
        return f"{self.first_name} {self.last_name}".strip() or "—"

    def get_email(self):
        """Return email, preferring the linked user account."""
        if self.user and self.user.email:
            return self.user.email
        return self.email

    def get_portrait_url(self):
        if self.portrait:
            return self.portrait.image_url
        return ""

    def __str__(self):
        return f"{self.get_full_name()} — {self.get_role_display()} @ {self.company}"
