from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey
from core.models import PageBase


class ButtonStyle(models.TextChoices):
    """Button style options"""

    PRIMARY = "primary", "Primary"
    SECONDARY = "secondary", "Secondary"
    OUTLINE = "outline", "Outline"
    GHOST = "ghost", "Ghost"
    ACCENT = "accent", "Accent"


class Button(PageBase):
    """
    Reusable button model that can be attached to any page component.
    Uses GenericForeignKey to allow attachment to any model.
    """

    # Generic relation to any model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.CharField(max_length=40, null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    # Store content type info as JSON for flexibility with UUIDs
    content_reference = models.JSONField(null=True, blank=True)

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
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Button"
        verbose_name_plural = "Buttons"

    def __str__(self):
        return self.text or "Untitled Button"

    def set_reference(self, instance):
        """Serialize the app_label, model_name, and object_id of a related instance."""
        content_type = ContentType.objects.get_for_model(instance)
        self.content_reference = {
            "app_label": content_type.app_label,
            "model_name": content_type.model,
            "object_id": str(instance.pk),
        }

    def save(self, *args, **kwargs):
        """Override save to automatically serialize the reference if content_object is set."""
        if self.content_object and not self.content_reference:
            self.set_reference(self.content_object)
        super().save(*args, **kwargs)


class PageComponent(models.Model):
    """
    Abstract base model for page components that can have buttons.
    All page sections (Hero, Features, Services, etc.) can inherit from this.
    """

    buttons = GenericRelation(Button, related_query_name="components")

    class Meta:
        abstract = True


class Page(MPTTModel):
    """
    Wagtail-like Page model with tree structure.
    """
    # Tree structure fields
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # Page identification
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    # Meta fields for SEO
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Override the title in search engine results",
    )
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="Description for search engines"
    )

    # Custom template (overrides page type template)
    custom_template = models.CharField(
        max_length=200,
        blank=True,
        help_text="Override the default template for this page"
    )

    # Page settings
    show_in_menus = models.BooleanField(
        default=False,
        help_text="Show this page in navigation menus"
    )
    menu_order = models.IntegerField(
        default=0,
        help_text="Order in navigation menus"
    )

    # Publishing
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    # Go live / expire dates
    go_live_at = models.DateTimeField(null=True, blank=True)
    expire_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_pages'
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_pages'
    )

    # Revision tracking
    revision_number = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['menu_order', 'title']

    class Meta:
        ordering = ['tree_id', 'lft']
        unique_together = ['parent', 'slug']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Get the URL for this page"""
        return reverse('pages:page', kwargs={'path': self.get_path()})

    def get_path(self):
        """Get the full path of the page"""
        return '/'.join([ancestor.slug for ancestor in self.get_ancestors(include_self=True)])

    @classmethod
    def get_root_page(cls):
        """
        Get the root page (page with no parent).
        Returns the most specific subclass instance if multiple root pages exist.
        """
        from django.db import connection

        # Try to get the root page using the most specific model first
        # Get all subclasses of Page
        subclasses = []
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
            # Also get nested subclasses
            for nested in subclass.__subclasses__():
                subclasses.append(nested)

        # Try each subclass in order of specificity (most specific first)
        for subclass in subclasses:
            try:
                page = subclass.objects.filter(
                    parent__isnull=True, is_published=True
                ).first()
                if page:
                    return page
            except Exception:
                pass

        # Fallback to generic Page
        try:
            return cls.objects.filter(parent__isnull=True, is_published=True).first()
        except cls.DoesNotExist:
            return None

    def get_template(self):
        """Get the template to use for rendering"""
        if self.custom_template:
            return self.custom_template
        # Default template based on slug
        return f"homepage/{self.slug}.html"

    def get_context(self, request=None):
        """Get additional context for rendering"""
        return {
            'page': self,
        }

    def serve(self, request):
        """Serve the page - can be overridden for custom rendering"""
        from django.shortcuts import render
        context = self.get_context(request)
        return render(request, self.get_template(), context)

    def get_specific(self):
        """
        Return the instance as its most specific subclass.
        Uses content types to find the specific instance.
        """
        # If it's already a subclass, return self
        if self.__class__ is not Page:
            return self

        # Otherwise, try to find the specific subclass
        # This is a simple implementation of multi-table inheritance retrieval
        for subclass in self.__class__.__subclasses__():
            try:
                specific_instance = getattr(self, subclass.__name__.lower())
                return specific_instance
            except (AttributeError, subclass.DoesNotExist):
                continue
        
        return self

    def save(self, *args, **kwargs):
        self.revision_number += 1
        super().save(*args, **kwargs)

    @property
    def status(self):
        """Get the status of the page"""
        if not self.is_published:
            return 'draft'
        if self.go_live_at and self.go_live_at > timezone.now():
            return 'scheduled'
        if self.expire_at and self.expire_at <= timezone.now():
            return 'expired'
        return 'published'
