"""
Views for AI Content Generation in Django Admin.
"""

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.utils.decorators import method_decorator

from .ai_service import ai_generator


@method_decorator(staff_member_required, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class AIContentGenerateView(View):
    """
    API endpoint for AI content generation in Django admin.

    Only accessible to staff members.
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON data"}, status=400
            )

        # Extract field context
        field_label = data.get("field_label", "Content")
        help_text = data.get("help_text", "")
        max_length = data.get("max_length")
        field_type = data.get("field_type", "TextField")
        custom_prompt = data.get("custom_prompt")
        related_values = data.get("related_values", {})

        # Use the enhanced generation method
        result = ai_generator.generate_field_content(
            field_label=field_label,
            help_text=help_text,
            max_length=max_length,
            field_type=field_type,
            custom_prompt=custom_prompt,
            related_values=related_values,
        )

        return JsonResponse(result)


# Function-based view for simpler URL configuration
@staff_member_required
@require_POST
def ai_generate_view(request):
    """
    Function-based view for AI content generation.

    This is an alternative to the class-based view above.
    Accepts field context including help_text, max_length, and custom prompts.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data"}, status=400
        )

    # Extract field context
    field_label = data.get("field_label", "Content")
    help_text = data.get("help_text", "")
    max_length = data.get("max_length")
    field_type = data.get("field_type", "TextField")
    custom_prompt = data.get("custom_prompt")
    related_values = data.get("related_values", {})

    # Use the enhanced generation method
    result = ai_generator.generate_field_content(
        field_label=field_label,
        help_text=help_text,
        max_length=max_length,
        field_type=field_type,
        custom_prompt=custom_prompt,
        related_values=related_values,
    )

    return JsonResponse(result)
