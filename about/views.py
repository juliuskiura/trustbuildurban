from django.shortcuts import render

from about.models import AboutPage, HeroSection, CorePillarsSection


def about(request):
    """Render the about page"""
    # Get the about page
    about_page = AboutPage.objects.filter(is_published=True).first()

    if not about_page:
        # Fallback to basic context if no published page
        return render(
            request,
            "about/about.html",
            {
                "meta": {
                    "title": "About | TrustBuild Urban",
                    "description": "Learn about our mission of radical transparency and excellence in construction.",
                }
            },
        )

    # Get sections
    hero_section = getattr(about_page, "hero_section", None)
    pillars_section = about_page.core_pillars_sections.first()

    # Build context from database
    context = {
        "meta": {
            "title": about_page.meta_title or "About | TrustBuild Urban",
            "description": about_page.meta_description
            or "Learn about our mission of radical transparency and excellence in construction.",
        }
    }

    # Hero section context
    if hero_section:
        story_stats = {}
        for stat in hero_section.stats.all():
            if stat.label == "Years Experience":
                story_stats["years_experience"] = {
                    "value": stat.value,
                    "label": stat.label,
                }
            elif stat.label == "Projects Completed":
                story_stats["projects_completed"] = {
                    "value": stat.value,
                    "label": stat.label,
                }

        context["story_section"] = {
            "eyebrow": hero_section.eyebrow,
            "heading": hero_section.heading,
            "description_1": hero_section.description,
            "description_2": "",
            "image_url": hero_section.image_url,
            "image_alt": hero_section.image_alt,
            "quote": hero_section.quote,
            "stats": story_stats,
        }

    # Pillars section context
    if pillars_section:
        pillars = []
        for pillar in pillars_section.pillars.all():
            pillars.append(
                {
                    "title": pillar.title,
                    "description": pillar.description,
                    "icon": pillar.icon,
                }
            )

        context["pillars_section"] = {
            "eyebrow": pillars_section.eyebrow,
            "heading": pillars_section.heading,
            "pillars": pillars,
        }

    return render(request, "about/about.html", context)
