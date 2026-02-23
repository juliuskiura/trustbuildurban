from django.shortcuts import render
from django.db.models import Prefetch

from .models import (
    ServicePage,
    ServicesHeader,
    ServicesListSection,
    Service,
)


def services(request):
    """Render the services page"""
    # Get the published ServicePage
    service_page = ServicePage.objects.filter(is_published=True).first()

    if not service_page:
        # Fallback to any service page
        service_page = ServicePage.objects.first()

    # Meta information from page
    meta = {
        "title": (
            service_page.meta_title
            if service_page
            else "Our Services | TrustBuild Urban"
        ),
        "description": (
            service_page.meta_description
            if service_page
            else "Specialized solutions in construction, project management, and structural engineering by TrustBuild Urban."
        ),
    }

    # Services header section
    services_header = None
    if service_page:
        header = getattr(service_page, "header_section", None)
        if header:
            services_header = {
                "eyebrow": header.eyebrow,
                "heading": header.heading,
                "description": header.description,
            }

    # Services list section
    services_list = None
    if service_page:
        services_section = service_page.services_sections.prefetch_related(
            Prefetch("services", queryset=Service.objects.order_by("order")),
        ).first()

        if services_section:
            # Get services
            services_items = []
            for service in services_section.services.all():
                # Get image URL
                image_url = service.image_url or (
                    service.image.image_url if service.image else None
                )

                services_items.append(
                    {
                        "icon": service.icon,
                        "title": service.title,
                        "description": service.description,
                        "image_url": image_url,
                        "link": service.link,
                    }
                )

            services_list = {
                "learn_more_text": services_section.learn_more_text,
                "services": services_items,
            }

    context = {
        "meta": meta,
        "services_header": services_header,
        "services_list": services_list,
    }

    return render(request, "services/services.html", context)
