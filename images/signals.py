"""
Django signals for automatic tracking of Image model usage.

This module provides signal handlers that automatically track when an Image
is used as a ForeignKey in any other model throughout the project.
"""

from django.db.models.signals import post_save, post_delete, m2m_changed
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.apps import apps

from images.models import Image, ImageUsage


# Registry of models that have ForeignKey to Image
# Format: {model_label: field_name}
# Example: {'blog.BlogPost': 'image', 'homepage.HeroSection': 'background_image'}
IMAGE_FOREIGN_KEY_MODELS = {}


def register_image_foreign_key(model_class, field_name):
    """
    Register a model that has a ForeignKey to Image.
    This should be called in the ready() method of the app's AppConfig.
    
    Args:
        model_class: The Django model class that has the ForeignKey
        field_name: The name of the ForeignKey field pointing to Image
    """
    model_label = f"{model_class._meta.app_label}.{model_class._meta.model_name}"
    IMAGE_FOREIGN_KEY_MODELS[model_label] = field_name


def get_image_field_from_instance(instance):
    """
    Find the Image ForeignKey field from an instance.
    
    Args:
        instance: Django model instance
        
    Returns:
        Field name if found, None otherwise
    """
    model_label = f"{instance._meta.app_label}.{instance._meta.model_name}"
    return IMAGE_FOREIGN_KEY_MODELS.get(model_label)


def update_image_usage_on_save(sender, instance, **kwargs):
    """
    Signal handler to track image usage when a model with an Image ForeignKey is saved.
    
    This creates an ImageUsage record when:
    - A new object with an Image ForeignKey is created
    - An existing object's Image ForeignKey is changed
    """
    field_name = get_image_field_from_instance(instance)

    if field_name is None:
        return

    try:
        image = getattr(instance, field_name, None)

        if image is None:
            # Image was removed, clean up usage record
            ImageUsage.objects.filter(
                content_type=ContentType.objects.get_for_model(instance),
                object_id=str(instance.pk),
            ).delete()
            return

        # Check if this image is actually an Image instance
        if not isinstance(image, Image):
            # It might be an ID
            try:
                image = Image.objects.get(pk=image)
            except Image.DoesNotExist:
                return

        content_type = ContentType.objects.get_for_model(instance)

        # Create or update usage record
        ImageUsage.objects.update_or_create(
            content_type=content_type,
            object_id=str(instance.pk),
            defaults={"image": image},
        )

    except Exception as e:
        # Silently handle errors to avoid disrupting normal model operations
        # In production, you might want to log these
        import logging
        logging.warning(f"Error updating image usage: {e}")
        pass


def update_image_usage_on_delete(sender, instance, **kwargs):
    """
    Signal handler to remove image usage when a model with an Image ForeignKey is deleted.
    """
    field_name = get_image_field_from_instance(instance)

    if field_name is None:
        return

    try:
        content_type = ContentType.objects.get_for_model(instance)

        # Remove usage record
        ImageUsage.objects.filter(
            content_type=content_type, object_id=str(instance.pk)
        ).delete()

    except Exception as e:
        import logging
        logging.warning(f"Error removing image usage: {e}")
        pass


def connect_signals():
    """
    Connect signal handlers to all registered models.
    Call this in the AppConfig.ready() method.
    """
    for model_label, field_name in IMAGE_FOREIGN_KEY_MODELS.items():
        try:
            # Get the model class
            app_label, model_name = model_label.split('.')
            model_class = apps.get_model(app_label, model_name)
            
            # Connect post_save signal
            post_save.connect(
                update_image_usage_on_save,
                sender=model_class,
                dispatch_uid=f"image_usage_save_{model_label}"
            )
            
            # Connect post_delete signal
            post_delete.connect(
                update_image_usage_on_delete,
                sender=model_class,
                dispatch_uid=f"image_usage_delete_{model_label}"
            )
            
        except LookupError:
            # Model not found, skip
            pass


# Decorator-based signal connection for cleaner code
def receiver_for_image_model(field_name):
    """
    Decorator to easily add signal handlers to models that have Image ForeignKeys.
    
    Usage:
        @receiver_for_image_model('image')
        class BlogPost(PageBase):
            image = models.ForeignKey(Image, on_delete=models.CASCADE)
    """
    def decorator(sender):
        model_label = f"{sender._meta.app_label}.{sender._meta.model_name}"
        IMAGE_FOREIGN_KEY_MODELS[model_label] = field_name
        
        post_save.connect(
            update_image_usage_on_save,
            sender=sender,
            dispatch_uid=f"image_usage_save_{model_label}"
        )
        
        post_delete.connect(
            update_image_usage_on_delete,
            sender=sender,
            dispatch_uid=f"image_usage_delete_{model_label}"
        )
        
        return sender
    return decorator
