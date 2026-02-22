from django.shortcuts import render


def guide(request):
    """Render the guides page"""
    # Meta information
    meta = {
        "title": "Diaspora Guide | TrustBuild Urban",
        "description": "The comprehensive blueprint for Kenyans living abroad to invest back home.",
    }

    # Guide hero section
    guide_hero = {
        "eyebrow": "Free Resource",
        "heading": "The Diaspora Building Blueprint 2024",
        "description": "Our comprehensive 40-page guide for Kenyans living abroad who want to invest in high-end real estate and custom home construction back home.",
        "features": [
            "Navigating Kenya's land laws and title verification.",
            "Current construction costs per square meter (Luxury vs. Mid-Market).",
            "How to legally supervise your project from thousands of miles away.",
            "Managing family expectations vs. professional project management.",
            "The legal requirements for NCA and County approvals.",
        ],
        "image_url": "https://images.unsplash.com/photo-1586769852836-bc069f19e1b6?auto=format&fit=crop&q=80&w=800",
        "image_alt": "Guide Preview",
        "form": {
            "title": "Enter your details to receive the PDF",
            "name_placeholder": "Full Name",
            "email_placeholder": "Email Address",
            "button_text": "DOWNLOAD NOW",
        },
        "social_proof": {
            "avatars": [
                "https://i.pravatar.cc/100?u=1",
                "https://i.pravatar.cc/100?u=2",
                "https://i.pravatar.cc/100?u=3",
                "https://i.pravatar.cc/100?u=4",
            ],
            "text": "Join 2,400+ Diaspora Investors",
            "verified_text": "Verified by AAK Architects",
        },
    }

    context = {
        "meta": meta,
        "guide_hero": guide_hero,
    }

    return render(request, "guides/guide.html", context)
