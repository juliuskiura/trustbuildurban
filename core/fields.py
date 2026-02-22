import string
import random

def generate_reference(prefix: str, length: int = 6):
    """
    Generate a random reference code.
    
    Args:
        prefix: Complete prefix including app and model initials with separators
        length: Length of random part
    """
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(characters, k=length))
    return f"{prefix}{random_part}"


from django.db import models, IntegrityError, transaction
from django.core.exceptions import ValidationError

class ReferenceField(models.CharField):
    """
    A custom field that generates a unique human-readable reference.
    
    Format options:
        - "app-model-X" : AC-UA-XXXXXX (separator between all parts)
        - "appmodelX"   : ACUAXXXXXX (no separators)
        - "app-modelX"  : AC-UAXXXXXX (separator between app & model only)
        - "appmodel-X"  : ACUA-XXXXXX (separator before random only)
    
    Usage:
        ReferenceField()  # Uses app name and model name from Django
        ReferenceField(app="AC", model="UA")  # Custom app and model
        ReferenceField(app="AC", model="UA", format="appmodelX")  # Custom format
    """

    def __init__(self, length=6, app=None, model=None, format="app-model-X", *args, **kwargs):
        self.length = length
        self.custom_app = app  # Custom app prefix override
        self.custom_model = model  # Custom model prefix override
        self.format = format
        
        # Calculate max_length based on format
        # App (2) + Model (2) + Random (length) + separators
        if format == "app-model-X":
            max_length = 2 + 1 + 2 + 1 + length  # AC-UA-XXXXXX
        elif format == "appmodelX":
            max_length = 2 + 2 + length  # ACUAXXXXXX
        elif format == "app-modelX":
            max_length = 2 + 1 + 2 + length  # AC-UAXXXXXX
        elif format == "appmodel-X":
            max_length = 2 + 2 + 1 + length  # ACUA-XXXXXX
        else:
            max_length = 2 + 1 + 2 + 1 + length  # default

        kwargs["max_length"] = max_length
        kwargs["unique"] = True
        kwargs["db_index"] = True
        kwargs["blank"] = True
        kwargs["null"] = True

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["length"] = self.length
        if self.custom_app:
            kwargs["app"] = self.custom_app
        if self.custom_model:
            kwargs["model"] = self.custom_model
        if self.format != "app-model-X":  # Only include if different from default
            kwargs["format"] = self.format
        return name, path, args, kwargs

    def get_prefix(self, model_instance):
        """
        Build the prefix based on app name, model name, and format.
        
        Returns prefixes like:
        - "AC-UA-" for format "app-model-X"
        - "ACUA" for format "appmodelX"
        - "AC-UA" for format "app-modelX"
        - "ACUA" for format "appmodel-X"
        """
        # Get app prefix (custom or from app label)
        if self.custom_app:
            app_prefix = self.custom_app.upper()
        else:
            app_prefix = model_instance._meta.app_label[:2].upper()
        
        # Get model prefix (custom or from model name)
        if self.custom_model:
            model_prefix = self.custom_model.upper()
        else:
            model_prefix = model_instance._meta.model_name[:2].upper()
        
        if self.format == "app-model-X":
            return f"{app_prefix}-{model_prefix}-"
        elif self.format == "appmodelX":
            return f"{app_prefix}{model_prefix}"
        elif self.format == "app-modelX":
            return f"{app_prefix}-{model_prefix}"
        elif self.format == "appmodel-X":
            return f"{app_prefix}{model_prefix}-"
        else:
            return f"{app_prefix}-{model_prefix}-"

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)

        if value:
            return value

        prefix = self.get_prefix(model_instance)
        reference = generate_reference(prefix, self.length)

        setattr(model_instance, self.attname, reference)
        return reference