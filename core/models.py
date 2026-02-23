from django.db import models
from django.db import models, IntegrityError, transaction
from django.db.models import Func


class PageBase(models.Model):
    """
    Abstract base model for page components.
    Provides common fields: uuid, created_at, updated_at
    """

    uuid = models.UUIDField(
        db_default=Func(function="uuidv7"),
        primary_key=True,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(models.Model):
    """
    An abstract base model that provides common fields for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    
    def save(self, *args, **kwargs):
        for _ in range(10):
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                if self._state.adding:
                    setattr(self, self.reference_field_name, None)
                    continue
                raise
        raise IntegrityError("Could not generate unique reference")
