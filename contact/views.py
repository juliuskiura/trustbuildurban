from django.shortcuts import render
from django.db.models import Prefetch

from .models import (
    ContactPage,
    ContactHeader,
    ContactContentSection,
    ContactInfo,
)


def contact(request):
    """Render the contact page"""
    # Get the published ContactPage
    contact_page = ContactPage.objects.filter(is_published=True).first()

    if not contact_page:
        # Fallback to any contact page
        contact_page = ContactPage.objects.first()

    # Meta information from page
    meta = {
        "title": (
            contact_page.meta_title if contact_page else "Contact Us | TrustBuild Urban"
        ),
        "description": (
            contact_page.meta_description
            if contact_page
            else "Get in touch with TrustBuild Urban for your premium construction and design projects in Kenya."
        ),
    }

    # Contact header section
    contact_header = None
    if contact_page:
        header = getattr(contact_page, "header_section", None)
        if header:
            contact_header = {
                "eyebrow": header.eyebrow,
                "heading": header.heading,
                "description": header.description,
            }

    # Contact content section
    contact_content = None
    if contact_page:
        content_section = getattr(contact_page, "content_section", None)
        if content_section:
            # Get info items
            info_items = []
            map_data = None

            for info in content_section.contact_info_items.all():
                # Check if this item has map data
                if info.map_embed_url:
                    map_data = {
                        "image_url": info.map_embed_url,
                        "alt_text": info.map_label or "Office Location",
                        "label": info.map_label or "Office Location",
                    }

                info_items.append(
                    {
                        "label": info.label,
                        "value": info.value,
                        "icon": info.icon,
                    }
                )

            # Get subject options from model choices
            from contact.models import SubjectChoice

            subject_options = [choice.label for choice in SubjectChoice]

            contact_content = {
                "form": {
                    "name_label": "Full Name",
                    "name_placeholder": "John Doe",
                    "email_label": "Email Address",
                    "email_placeholder": "john@example.com",
                    "subject_label": "Subject",
                    "subject_options": subject_options,
                    "message_label": "Your Message",
                    "message_placeholder": "Tell us about your project...",
                    "submit_text": "Send Message",
                },
                "info": {
                    "title": content_section.heading or "Contact Information",
                    "items": info_items,
                    "map": map_data,
                },
            }

    context = {
        "meta": meta,
        "contact_header": contact_header,
        "contact_content": contact_content,
    }

    return render(request, "contact/contact.html", context)
