from django.shortcuts import render, get_object_or_404
from .models import AvailableHome


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

    return render(request, "available_homes/available.html", {"pagedata": pagedata, "homes": homes})


def property_detail_test(request):
    """
    Temporary view to test the property detail page design.
    """
    return render(request, "available_homes/property_detail_page.html")


def property_detail(request, slug):
    """
    View function for the property detail page.
    Fetches data from the database models.
    """    

    # Fetch the property from the database
    property = get_object_or_404(AvailableHome, slug=slug)

    # Fetch related data for partial templates
    bathroom_info = property.bathroom_information.all()
    bedroom_info = property.bedroom_information.all()
    heating_and_cooling_info = property.heating_and_cooling.all()
    kitchen_and_dining_info = property.kitchen_and_dining.all()
    interior_features_info = property.interior_features.all()
    other_rooms_info = property.other_rooms.all()
    garage_and_parking_info = property.garage_and_parking.all()
    utilities_and_green_energy_info = property.utilities_and_green_energy.all()
    outdoor_spaces_info = property.outdoor_spaces.all()

    context = {
        "object": property,
        "bathroom_info": bathroom_info,
        "bedroom_info": bedroom_info,
        "heating_and_cooling_info": heating_and_cooling_info,
        "kitchen_and_dining_info": kitchen_and_dining_info,
        "interior_features_info": interior_features_info,
        "other_rooms_info": other_rooms_info,
        "garage_and_parking_info": garage_and_parking_info,
        "utilities_and_green_energy_info": utilities_and_green_energy_info,
        "outdoor_spaces_info": outdoor_spaces_info,
    }

    return render(request, "available_homes/property_detail.html", context)
