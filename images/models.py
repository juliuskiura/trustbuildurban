from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from core.models import PageBase


class Image(PageBase):
    """
    Reusable image model that can be attached to any page component.
    Uses GenericForeignKey to allow attachment to any model.
    """
    # Generic relation to any model
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='images'
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Image data
    image = models.ImageField(upload_to='images/', blank=True)
    url = models.URLField(max_length=500, blank=True, help_text="External image URL")
    
    # Alt text and caption
    alt_text = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    
    # Image metadata
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    
    # Usage settings
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
    
    def __str__(self):
        return self.alt_text or f"Image {self.pk}"
    
    @property
    def image_url(self):
        """Return image URL - prefers uploaded image, falls back to URL"""
        if self.image:
            return self.image.url
        return self.url
