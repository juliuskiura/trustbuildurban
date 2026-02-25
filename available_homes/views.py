from django.shortcuts import render


def available_homes(request):
    """
    View function for the Available Homes page.
    Fetches data from the database models.
    """
    from available_homes.models import (
        AvailableHomesPage,
        AvailableHomesHeroSection,
        AvailableHomesCTASection,
        AvailableHome,
    )

    # Get the published AvailableHomesPage
    page = AvailableHomesPage.objects.filter(is_published=True).first()

    # Build the context
    pagedata = {
        "herosection": {
            "title": "Available Homes For Sale",
            "description": "High-quality homes built by TrustBuildUrban for immediate purchase. Move-in ready residences in Kenya's most sought-after neighborhoods.",
        },
        "homes": [],
        "cta_Section": {
            "title": "Didn't find what you're looking for?",
            "description": "We can design and build a bespoke home specifically for you on your preferred piece of land.",
            "buttonText": "LEARN ABOUT CUSTOM BUILD",
            "buttonLink": "/process/",
        },
    }

    # If page exists, fetch hero section data
    if page:
        hero_section = getattr(page, "hero_section", None)
        if hero_section:
            pagedata["herosection"] = {
                "title": hero_section.title,
                "description": hero_section.description,
            }

        # Fetch CTA section data
        cta_section = getattr(page, "cta_section", None)
        if cta_section:
            pagedata["cta_Section"] = {
                "title": cta_section.title,
                "description": cta_section.description,
                "buttonText": cta_section.button_text,
                "buttonLink": cta_section.button_link,
            }

    # Fetch all available homes from the database
    homes = AvailableHome.objects.all().order_by("order")

    # Build homes list
    for home in homes:
        pagedata["homes"].append(
            {
                "id": str(home.uuid),
                "title": home.title,
                "location": home.location,
                "price": home.price,
                "beds": home.beds,
                "baths": home.baths,
                "sqft": home.sqft,
                "status": home.get_status_display_custom(),
                "imageUrl": home.get_image_url() or "",
            }
        )

    return render(request, "available_homes/available.html", {"pagedata": pagedata})


def property_detail_test(request):
    """
    Temporary view to test the property detail page design.
    """
    return render(request, "available_homes/property_detail_page.html")
