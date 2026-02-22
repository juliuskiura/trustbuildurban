from django.shortcuts import render


def services(request):
    """Render the services page"""
    # Meta information
    meta = {
        "title": "Our Services | TrustBuild Urban",
        "description": "Specialized solutions in construction, project management, and structural engineering by TrustBuild Urban.",
    }

    # Services header section
    services_header = {
        "eyebrow": "What We Do",
        "heading": "Specialized Solutions for Discerning Clients.",
        "description": "From the first site visit to the final coat of paint, we manage the complexities of construction so you don't have to.",
    }

    # Services list section
    services_list = {
        "learn_more_text": "Learn More",
        "services": [
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-globe w-10 h-10" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>""",
                "title": "Consultancy",
                "description": "Expert advice for your building project. We handle all the heavy lifting, ensuring your project meets both local regulations and international standards.",
                "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a?auto=format&fit=crop&q=80&w=1200",
            },
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-house w-10 h-10" aria-hidden="true"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"></path><path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>""",
                "title": "Construction",
                "description": "Quality builds you can trust. We manage master craftsmen and premium materials to ensure your legacy is built to the highest possible standards.",
                "image_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&q=80&w=1200",
            },
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-settings w-10 h-10" aria-hidden="true"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>""",
                "title": "Project Management",
                "description": "We manage everything for you. From procurement to labor management, we act as your local eyes and ears, treating your investment with the same care as our own.",
                "image_url": "https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=1200",
            },
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search w-10 h-10" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>""",
                "title": "Site Inspection",
                "description": "Regular checks on your progress. We provide detailed reports and live video updates, ensuring radical transparency throughout the building lifecycle.",
                "image_url": "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&q=80&w=1200",
            },
        ],
    }

    context = {
        "meta": meta,
        "services_header": services_header,
        "services_list": services_list,
    }

    return render(request, "services/services.html", context)
