"""
Custom middleware for Django admin.
"""

from django.conf import settings


class AdminCustomCSSMiddleware:
    """
    Middleware to inject custom CSS into the admin interface.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only inject on admin pages
        if request.path.startswith("/admin/"):
            # Check if we need to add custom CSS
            # This is a placeholder for custom admin CSS
            pass

        return response
