from django.db import models
from django.db import models, IntegrityError, transaction
# Create your models here.
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