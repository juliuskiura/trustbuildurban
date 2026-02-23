from django.db import models
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
        """Extract alt_text and caption from image EXIF data if not provided."""
        from PIL import Image as PILImage
        import io

        # Extract metadata from uploaded image if available
        if self.image:
            try:
                # Open the image file
                if hasattr(self.image, "path"):
                    img = PILImage.open(self.image.path)
                elif hasattr(self.image, "file"):
                    img = PILImage.open(self.image.file)
                else:
                    img = None

                if img:
                    # Get image dimensions
                    self.width, self.height = img.size

                    # Try to extract EXIF data
                    exif_data = img.getexif()

                    # Extract alt_text from EXIF if not provided
                    if not self.alt_text:
                        # Try common EXIF tags for description/alt text
                        # 0x010E = ImageDescription
                        # 0x9286 = UserComment
                        # 0xFDE9 = OwnerName (sometimes used for captions)
                        alt_text_sources = [
                            exif_data.get(0x010E),  # ImageDescription
                            exif_data.get(0x9286),  # UserComment
                        ]
                        for source in alt_text_sources:
                            if source:
                                # Decode if bytes
                                if isinstance(source, bytes):
                                    try:
                                        source = source.decode("utf-8", errors="ignore")
                                    except:
                                        continue
                                if source and source.strip():
                                    self.alt_text = source.strip()[:200]
                                    break

                        # If still no alt_text, use filename as fallback
                        if not self.alt_text and hasattr(self.image, "name"):
                            filename = self.image.name
                            if filename:
                                # Remove extension and underscores, capitalize words
                                name_without_ext = (
                                    filename.rsplit(".", 1)[0]
                                    if "." in filename
                                    else filename
                                )
                                self.alt_text = (
                                    name_without_ext.replace("_", " ")
                                    .replace("-", " ")
                                    .title()
                                )

                    # Extract caption from EXIF if not provided
                    if not self.caption:
                        # Try to get caption from XPComment (more common in Windows)
                        # or from other metadata
                        caption_sources = [
                            exif_data.get(0x9286),  # UserComment
                            exif_data.get(0x010E),  # ImageDescription
                        ]
                        for source in caption_sources:
                            if source:
                                if isinstance(source, bytes):
                                    try:
                                        source = source.decode("utf-8", errors="ignore")
                                    except:
                                        continue
                                if source and source.strip():
                                    self.caption = source.strip()[:200]
                                    break
            except Exception:
                # If anything goes wrong with EXIF extraction, continue without it
                pass

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
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="image_usages"
    )
    object_id = models.PositiveIntegerField()
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

    @property
    def used_object(self):
        """Return the actual object that uses this image."""
        return self.content_object
