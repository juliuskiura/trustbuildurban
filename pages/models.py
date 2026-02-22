from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


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
    
      # SEO fields
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Override the title in search engine results"
    )
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Description for search engines"
    )

    # Content fields
    introduction = models.TextField(blank=True)
    body = models.TextField(blank=True, help_text="Main content of the page")
    
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
