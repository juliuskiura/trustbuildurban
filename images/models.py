from django.db import models
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
