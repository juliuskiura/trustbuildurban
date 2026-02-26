from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

from .models import (
    ContactPage,
    ContactHeader,
    ContactContentSection,
    ContactSubmission,
    SubjectChoice,
)

logger = logging.getLogger(__name__)


def contact(request):
    """Render the contact page."""
    contact_page = ContactPage.objects.filter(is_published=True).first()
    if not contact_page:
        contact_page = ContactPage.objects.first()

    meta = {
        "title": (
            contact_page.meta_title
            if contact_page
            else "Contact Us | AnchorFields Ltd"
        ),
        "description": (
            contact_page.meta_description
            if contact_page
            else "Get in touch with AnchorFields Ltd for premium home building in Kenya."
        ),
    }

    contact_header = None
    if contact_page:
        header = getattr(contact_page, "header_section", None)
        if header:
            contact_header = {
                "eyebrow": header.eyebrow,
                "heading": header.heading,
                "description": header.description,
            }

    contact_content = {
        "form": {
            "name_label": "Full Name",
            "name_placeholder": "John Doe",
            "email_label": "Email Address",
            "email_placeholder": "john@example.com",
            "subject_label": "Subject",
            "subject_options": [choice.label for choice in SubjectChoice],
            "message_label": "Your Message",
            "message_placeholder": "Tell us about your project…",
            "submit_text": "Send Message",
        },
        "info": {
            "title": "Contact Information",
            "items": [],   # now driven by company context processor
            "map": True,   # signals the template to render the map block
        },
    }

    return render(
        request,
        "contact/contact.html",
        {
            "meta": meta,
            "contact_header": contact_header,
            "contact_content": contact_content,
        },
    )


@require_http_methods(["POST"])
def submit_contact(request):
    """
    Handle contact-form submissions via AJAX (mirrors the showing/offer pattern).
    Applies a honeypot check for bot protection.
    """
    from .forms import ContactSubmissionForm

    # ── Honeypot guard ────────────────────────────────────────────────────
    if request.POST.get("website_url", ""):
        # Bots fill every field; real users leave this hidden field blank
        logger.warning("Contact form honeypot triggered — discarding submission")
        # Return a fake success so bots don't retry
        return JsonResponse(
            {"success": True, "message": "Thank you! We'll be in touch."}
        )

    form = ContactSubmissionForm(request.POST)

    if form.is_valid():
        submission = form.save()
        logger.info(f"Contact submission saved: {submission.pk}")
        return JsonResponse(
            {
                "success": True,
                "message": "Message received! We'll get back to you within 24 hours.",
            }
        )

    logger.warning(f"Contact form validation errors: {form.errors}")
    errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
    return JsonResponse(
        {
            "success": False,
            "message": "Please correct the errors below.",
            "errors": errors,
        },
        status=400,
    )
