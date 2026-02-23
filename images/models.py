from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import PageBase


class Image(PageBase):
    """
    Reusable image model that can be attached to any page component.
    """

    # Image data
    image = models.ImageField(upload_to='images/', blank=True)
    url = models.URLField(max_length=500, blank=True, help_text="External image URL")

    # Alt text and caption
    alt_text = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)

    # Image metadata
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.alt_text or f"Image {self.pk}"

    @property
    def usage_count(self):
        """
        Return the total number of times this image is used as a foreign key
        across all models.
        """
        if self._state.adding:
            return 0
        return ImageUsage.objects.filter(image=self).count()

    @property
    def used_by_models(self):
        """
        Return a list of model names that use this image.
        """
        if self._state.adding:
            return []
        return list(
            ImageUsage.objects.filter(image=self)
            .values_list("content_type__model", flat=True)
            .distinct()
        )

    @property
    def usage_details(self):
        """
        Return detailed usage information grouped by model.
        """
        if self._state.adding:
            return []
        from django.db.models import Count

        return (
            ImageUsage.objects.filter(image=self)
            .values("content_type__model")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    @property
    def image_url(self):
        """Return image URL - prefers uploaded image, falls back to URL"""
        if self.image:
            return self.image.url
        return self.url

    def save(self, *args, **kwargs):
        """Extract alt_text, caption, width, height from image if not provided."""
        from PIL import Image as PILImage
        import os

        # Extract metadata from uploaded image if available
        if self.image:
            try:
                img = None

                # Try different ways to open the image
                # Method 1: For files uploaded through Django admin
                if hasattr(self.image, "temporary_file_path"):
                    temp_path = self.image.temporary_file_path()
                    if temp_path and os.path.exists(temp_path):
                        img = PILImage.open(temp_path)

                # Method 2: Check if image has a path attribute
                if not img and hasattr(self.image, "path") and self.image.path:
                    if os.path.exists(self.image.path):
                        img = PILImage.open(self.image.path)

                # Method 3: Check if image has a file attribute
                if not img and hasattr(self.image, "file") and self.image.file:
                    try:
                        self.image.file.seek(0)
                        img = PILImage.open(self.image.file)
                    except:
                        pass

                # Method 4: Try name attribute (Django stores the filename here)
                if not img and hasattr(self.image, "name") and self.image.name:
                    # The name contains the upload_to path, try to construct full path
                    full_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
                    if os.path.exists(full_path):
                        img = PILImage.open(full_path)

                if img:
                    # Get image dimensions
                    self.width, self.height = img.size

                    # Extract alt_text from filename as primary source
                    if not self.alt_text and hasattr(self.image, "name"):
                        filename = self.image.name
                        if filename:
                            name_without_path = os.path.basename(filename)
                            name_without_ext = os.path.splitext(name_without_path)[0]
                            self.alt_text = (
                                name_without_ext.replace("_", " ")
                                .replace("-", " ")
                                .title()
                            )

                    # Extract caption from filename if not provided
                    if not self.caption and hasattr(self.image, "name"):
                        filename = self.image.name
                        if filename:
                            name_without_path = os.path.basename(filename)
                            name_without_ext = os.path.splitext(name_without_path)[0]
                            self.caption = (
                                name_without_ext.replace("_", " ")
                                .replace("-", " ")
                                .title()
                            )

                    # Try to extract EXIF data as secondary source
                    try:
                        exif_data = img.getexif()

                        # Override with EXIF if available and user didn't provide values
                        if not self.alt_text:
                            exif_alt = exif_data.get(0x010E) or exif_data.get(0x9286)
                            if exif_alt:
                                if isinstance(exif_alt, bytes):
                                    exif_alt = exif_alt.decode("utf-8", errors="ignore")
                                if exif_alt and exif_alt.strip():
                                    self.alt_text = exif_alt.strip()[:200]

                        if not self.caption:
                            exif_caption = exif_data.get(0x9286) or exif_data.get(
                                0x010E
                            )
                            if exif_caption:
                                if isinstance(exif_caption, bytes):
                                    exif_caption = exif_caption.decode(
                                        "utf-8", errors="ignore"
                                    )
                                if exif_caption and exif_caption.strip():
                                    self.caption = exif_caption.strip()[:200]
                    except:
                        pass

            except Exception as e:
                # Log the error for debugging but don't break the save
                import logging

                logger = logging.getLogger(__name__)
                logger.error(f"Error extracting image metadata: {e}")

        super().save(*args, **kwargs)


class ImageUsage(models.Model):
    """
    Tracks usage of Image model across all foreign key relationships.

    This model automatically records when an Image is used as a ForeignKey
    in any other model throughout the project. It provides:
    - Total usage count per image
    - Breakdown by content type (which model is using it)
    - Automatic tracking via Django signals

    Usage example:
        # Get usage count for an image
        image = Image.objects.get(pk=1)
        print(f"Used {image.usage_count} times")

        # Get which models use this image
        print(f"Used in: {image.used_by_models}")

        # Get detailed usage
        for usage in image.usage_details:
            print(f"  {usage['content_type__model']}: {usage['count']} times")
    """

    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="usage_records"
    )
    # Store content type info as JSON for flexibility with UUIDs
    content_reference = models.JSONField(null=True, blank=True)
    # Keep legacy fields for backward compatibility
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="image_usages",
        null=True,
        blank=True,
    )
    object_id = models.CharField(max_length=40, null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Image Usage"
        verbose_name_plural = "Image Usages"
        unique_together = ["content_type", "object_id", "image"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["image"]),
        ]

    def __str__(self):
        return f"{self.image} used in {self.content_type.model} (ID: {self.object_id})"

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

    @property
    def used_object(self):
        """Return the actual object that uses this image."""
        return self.content_object
