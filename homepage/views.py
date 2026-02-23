from django.shortcuts import render
from django.http import Http404
from .models import (
    Page,
    HomePage,
    HeroSection,
    Stats,
    StatsSection,
    ClientReview,
    DiasporaSection,
    DiasporaChallenge,
    FeaturesSection,
    Feature,
    StepsSection,
    Step,
    ServicesSection,
    Service,
    NewsletterSection,
)


def index(request):
    # Get the homepage
    homepage = (
        HomePage.objects.select_related("hero_section")
        .prefetch_related(
            "hero_section__stats",
            "stats_sections",
            "stats_sections__client_reviews",
            "diaspora_sections",
            "diaspora_sections__challenges",
            "features_sections",
            "features_sections__features",
            "steps_sections",
            "steps_sections__steps",
            "services_sections",
            "services_sections__services",
            "newsletter_sections",
            "newsletter_sections__buttons",
        )
        .filter(is_published=True)
        .first()
    )

    if not homepage:
        homepage = HomePage.objects.first()

    # Meta information
    meta = {
        "title": "CivicCore Engineering | Premium Consultancy",
        "description": "Engineering excellence from the ground up. We deliver innovative structural design, project management, and sustainable engineering solutions.",
    }

    # Hero section data from model
    hero = {
        "tagline": "",
        "heading_main": "",
        "heading_highlight": "",
        "heading_suffix": "",
        "description": "",
        "cta_primary_text": "Get Started",
        "cta_secondary_text": "Watch video",
        "image_url": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&q=80&w=1200",
        "verified_text": "Verified",
        "live_tracking_text": "Live Project Tracking",
        "company_name": "TrustBuild",
        "company_location": "Nairobi, Kenya",
        "stats": {},
    }

    hero_section = getattr(homepage, "hero_section", None)
    if hero_section:
        hero = {
            "tagline": hero_section.tagline,
            "heading_main": hero_section.heading_main,
            "heading_highlight": hero_section.heading_highlight,
            "heading_suffix": hero_section.heading_suffix,
            "description": hero_section.description,
            "cta_primary_text": "Get Started",
            "cta_secondary_text": "Watch video",
            "image_url": (
                hero_section.background_image.image_url
                if hero_section.background_image
                else ""
            ),
            "verified_text": hero_section.verified_text,
            "live_tracking_text": hero_section.live_tracking_text,
            "company_name": hero_section.company_name,
            "company_location": hero_section.company_location,
            "show_verified_badge": hero_section.show_verified_badge,
            "show_live_tracking": hero_section.show_live_tracking,
            "stats": {},
        }
        # Get hero stats (already prefetched)
        for stat in hero_section.stats.all():
            hero["stats"][stat.label.lower().replace(" ", "_")] = {
                "value": stat.value,
                "label": stat.label,
            }

    # Stats section data from model
    stats_section_data = {
        "quote_text": "Integrity and innovation in every structure we touch. Engineering excellence from the ground up.",
        "landmark_projects": {"value": "850", "label_text": "Landmark Projects"},
        "client_reviews": {
            "rating": 5,
            "total_reviews": "12,000+",
            "label_text": "Client Reviews",
            "button_text": "Discover Excellence",
            "button_link": "#",
        },
    }

    stats_section_obj = getattr(homepage, "stats_sections", None)
    if stats_section_obj and stats_section_obj.exists():
        stats_section_obj = stats_section_obj.first()
        stats_section_data = {
            "quote_text": stats_section_obj.quote_text,
            "landmark_projects": {
                "value": stats_section_obj.landmark_projects_value,
                "label_text": stats_section_obj.landmark_projects_label_text,
            },
            "client_reviews": {},
        }
        # Get client reviews (already prefetched)
        client_review = stats_section_obj.client_reviews.first()
        if client_review:
            stats_section_data["client_reviews"] = {
                "rating": client_review.rating,
                "total_reviews": client_review.total_reviews,
                "label_text": client_review.label_text,
                "button_text": client_review.button_text,
                "button_link": client_review.button_link,
            }

    # Diaspora section data from model
    diaspora_section_data = {
        "eyebrow": "The Diaspora Challenge",
        "heading": "Building in Kenya should not be a gamble.",
        "challenges": [],
        "attribution": "TrustBuildUrban was founded to replace fear with structured, world-class building standards.",
        "featured_project": {
            "label": "Featured Project",
            "title": "The Grand Residence, Runda",
            "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?q=80&w=870&auto=format&fit=crop",
        },
    }

    diaspora_section = getattr(homepage, "diaspora_sections", None)
    if diaspora_section and diaspora_section.exists():
        diaspora_section = diaspora_section.first()
        diaspora_section_data = {
            "eyebrow": diaspora_section.eyebrow,
            "heading": diaspora_section.heading,
            "attribution": diaspora_section.attribution,
            "challenges": [],
            "featured_project": {
                "label": diaspora_section.featured_label,
                "title": diaspora_section.featured_title,
                "image_url": (
                    diaspora_section.featured_image.image_url
                    if diaspora_section.featured_image
                    else diaspora_section.featured_image_url
                ),
            },
        }
        # Get challenges (already prefetched)
        for challenge in diaspora_section.challenges.all():
            diaspora_section_data["challenges"].append(
                {
                    "title": challenge.title,
                    "description": challenge.description,
                }
            )

    # Features section data from model
    features_section_data = {
        "eyebrow": "The TrustBuildUrban Standard",
        "heading": "Why Hundreds of Diaspora Families Trust Us",
        "features": [],
    }

    features_section = getattr(homepage, "features_sections", None)
    if features_section and features_section.exists():
        features_section = features_section.first()
        features_section_data = {
            "eyebrow": features_section.eyebrow,
            "heading": features_section.heading,
            "features": [],
        }
        # Get features (already prefetched)
        for feature in features_section.features.all():
            features_section_data["features"].append(
                {
                    "title": feature.title,
                    "description": feature.description,
                    "icon_path": feature.icon_path,
                }
            )

    # Steps section data from model
    steps_section_data = {
        "eyebrow": "Transparent Execution",
        "heading": "Our 7-Step Architectural Journey",
        "description": "A meticulously structured process from initial concept to the day we hand over your keys.",
        "steps": [],
    }

    steps_section = getattr(homepage, "steps_sections", None)
    if steps_section and steps_section.exists():
        steps_section = steps_section.first()
        steps_section_data = {
            "eyebrow": steps_section.eyebrow,
            "heading": steps_section.heading,
            "description": steps_section.description,
            "steps": [],
        }
        # Get steps (already prefetched)
        for step in steps_section.steps.all():
            steps_section_data["steps"].append(
                {
                    "title": step.title,
                    "description": step.description,
                }
            )

    # Services section data from model
    services_section_data = {
        "subtitle": "Our Specializations",
        "heading": "Elite Engineering & Architectural Excellence",
        "services": [],
    }

    services_section = getattr(homepage, "services_sections", None)
    if services_section and services_section.exists():
        services_section = services_section.first()
        services_section_data = {
            "subtitle": services_section.subtitle,
            "heading": services_section.heading,
            "services": [],
        }
        # Get services (already prefetched)
        for service in services_section.services.all():
            # Parse expertise from comma-separated string to list
            expertise_list = []
            if service.expertise:
                expertise_list = [e.strip() for e in service.expertise.split(",")]

            services_section_data["services"].append(
                {
                    "title": service.title,
                    "description": service.description,
                    "icon": service.icon,
                    "expertise": expertise_list,
                }
            )

    # Newsletter section data from model
    newsletter_data = {
        "heading": "Free Diaspora Home Building Guide",
        "description": "Download our comprehensive manual on navigating land laws, approvals, and construction costs in Kenya from abroad.",
        "cta_text": "GET THE GUIDE",
        "placeholder": "Enter your email",
    }

    newsletter_section = getattr(homepage, "newsletter_sections", None)
    if newsletter_section and newsletter_section.exists():
        newsletter_section = newsletter_section.first()
        newsletter_data = {
            "heading": newsletter_section.heading,
            "description": newsletter_section.description,
            "placeholder": newsletter_section.placeholder,
            "cta_text": "GET THE GUIDE",
        }
        # Get CTA button if exists (already prefetched)
        cta_button = newsletter_section.buttons.first()
        if cta_button:
            newsletter_data["cta_text"] = cta_button.text

    # Portfolio section - Keep as is (hardcoded fallback)
    portfolio_section = {
        "heading": "Portfolio Highlights",
        "description": "Luxury and family homes delivered across the country.",
        "view_all_text": "View All Projects",
        # Fallback properties when no available_properties in context
        "fallback_properties": [
            {
                "title": "The Azure Villa",
                "location": "Runda, Nairobi",
                "type": "Luxury",
                "duration": "14 Months",
                "image_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&q=80&w=800",
            },
            {
                "title": "Oasis Heights",
                "location": "Karen, Nairobi",
                "type": "Villa",
                "duration": "12 Months",
                "image_url": "https://images.unsplash.com/photo-1616012760010-8da02da071fd?q=80&w=1032",
            },
            {
                "title": "Serene Ridge Estate",
                "location": "Tatu City, Kiambu",
                "type": "Family Home",
                "duration": "10 Months",
                "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=800",
            },
        ],
    }

    context = {
        # Meta
        "meta": meta,
        # Hero
        "hero": hero,
        # Stats
        "stats_section": stats_section_data,
        # Sections from models
        "diaspora_section": diaspora_section_data,
        "features_section": features_section_data,
        "steps_section": steps_section_data,
        "services_section": services_section_data,
        # Portfolio - kept as is
        "portfolio_section": portfolio_section,
        # Newsletter
        "newsletter": newsletter_data,
        "star_range": list(range(1, 6)),
    }

    return render(request, "homepage/index.html", context)


def page_detail(request, path=None):
    """
    Serve a page based on its path from the database.
    Uses the Page model to render dynamic pages.
    """
    # If no path provided, use the Page model's get_root_page method
    if not path:
        from pages.models import Page

        page = Page.get_root_page()
        if page:
            return page.serve(request)
        raise Http404("No root page found")

    # Split the path into segments
    path_segments = path.strip('/').split('/')

    # Try to find the page by slug chain
    try:
        # Get all pages at the root level matching the first segment
        page = Page.objects.get(slug=path_segments[0], parent__isnull=True, is_published=True)

        # Navigate down the tree
        for segment in path_segments[1:]:
            page = Page.objects.get(slug=segment, parent=page, is_published=True)

        return page.serve(request)

    except Page.DoesNotExist:
        raise Http404(f"Page not found: {path}")


def page_by_id(request, page_id):
    """Serve a page by its ID (fallback method)."""
    from django.shortcuts import get_object_or_404
    page = get_object_or_404(Page, pk=page_id, is_published=True)
    return page.serve(request)


def preview_page(request, page_id):
    """Preview a page (even if not published)."""
    from django.shortcuts import get_object_or_404
    from django.contrib.auth.decorators import login_required
    
    page = get_object_or_404(Page, pk=page_id)
    
    # Check permissions
    if not request.user.has_perm('homepage.change_page'):
        raise Http404("You don't have permission to preview this page")
    
    return page.serve(request)
