from django.shortcuts import render


def about(request):
    """Render the about page"""
    # Meta information
    meta = {
        "title": "About | TrustBuild Urban",
        "description": "Learn about our mission of radical transparency and excellence in construction.",
    }

    # Story section data (hero section)
    story_section = {
        "eyebrow": "Our Story",
        "heading": "Excellence in Construction, Built on Trust.",
        "description_1": "Founded on the principle of radical transparency, TrustBuild Urban has become the premier choice for Kenyans living abroad and local high-end homeowners. We recognized a massive gap in the market: the lack of corporate accountability in residential construction.",
        "description_2": "Our mission is to provide a seamless, stress-free building experience where quality is never compromised, and every shilling is accounted for. We don't just build houses; we build legacies.",
        "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a?auto=format&fit=crop&q=80&w=1200",
        "image_alt": "Architecture Team",
        "quote": "Transparency isn't a buzzword; it's our core architecture.",
        "stats": {
            "years_experience": {
                "value": "10+",
                "label": "Years Experience",
            },
            "projects_completed": {
                "value": "150+",
                "label": "Projects Completed",
            },
        },
    }

    # Core Pillars section data
    pillars_section = {
        "eyebrow": "The TrustBuild Standards",
        "heading": "Our Core Pillars",
        "pillars": [
            {
                "title": "Uncompromising Quality",
                "description": "We source premium materials and employ master craftsmen to ensure every finish is world-class.",
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-award w-8 h-8" aria-hidden="true"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"></path><circle cx="12" cy="8" r="6"></circle></svg>""",
            },
            {
                "title": "Client Partnership",
                "description": "We act as your local eyes and ears, treating your investment with the same care as our own.",
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users w-8 h-8" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><path d="M16 3.128a4 4 0 0 1 0 7.744"></path><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><circle cx="9" cy="7" r="4"></circle></svg>""",
            },
            {
                "title": "Ethical Conduct",
                "description": "From legal land acquisition to labor management, we operate with absolute integrity.",
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-check-big w-8 h-8" aria-hidden="true"><path d="M21.801 10A10 10 0 1 1 17 3.335"></path><path d="m9 11 3 3L22 4"></path></svg>""",
            },
        ],
    }

    context = {
        "meta": meta,
        "story_section": story_section,
        "pillars_section": pillars_section,
    }

    return render(request, "about/about.html", context)
