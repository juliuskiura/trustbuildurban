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

        prompt_type = data.get("prompt_type", "generic")
        context = data.get("context", {})
        field_name = data.get("field_name", "")

        # Route to appropriate generation method based on prompt type
        if prompt_type == "hero_description":
            result = ai_generator.generate_hero_description(
                tagline=context.get("tagline"),
                heading_main=context.get("heading_main"),
                company_name=context.get("company_name", "TrustBuildUrban"),
            )
        else:
            # Generic content generation
            prompt = data.get("prompt", "Generate content for this field.")
            result = ai_generator.generate_content(
                prompt=prompt, context=json.dumps(context) if context else None
            )

        return JsonResponse(result)


# Function-based view for simpler URL configuration
@staff_member_required
@require_POST
def ai_generate_view(request):
    """
    Function-based view for AI content generation.

    This is an alternative to the class-based view above.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data"}, status=400
        )

    prompt_type = data.get("prompt_type", "generic")
    context = data.get("context", {})

    # Route to appropriate generation method based on prompt type
    if prompt_type == "hero_description":
        result = ai_generator.generate_hero_description(
            tagline=context.get("tagline"),
            heading_main=context.get("heading_main"),
            company_name=context.get("company_name", "TrustBuildUrban"),
        )
    else:
        # Generic content generation
        prompt = data.get("prompt", "Generate content for this field.")
        result = ai_generator.generate_content(
            prompt=prompt, context=json.dumps(context) if context else None
        )

    return JsonResponse(result)
