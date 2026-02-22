from django.shortcuts import render


def contact(request):
    """Render the contact page"""
    # Meta information
    meta = {
        "title": "Contact Us | TrustBuild Urban",
        "description": "Get in touch with TrustBuild Urban for your premium construction and design projects in Kenya.",
    }

    # Contact header section
    contact_header = {
        "eyebrow": "Get In Touch",
        "heading": "Let's Build Your Legacy Together.",
        "description": "Whether you're in the diaspora or local, we're here to provide the radical transparency and excellence your project deserves.",
    }

    # Contact content section
    contact_content = {
        "form": {
            "name_label": "Full Name",
            "name_placeholder": "John Doe",
            "email_label": "Email Address",
            "email_placeholder": "john@example.com",
            "subject_label": "Subject",
            "subject_options": [
                "New Project Inquiry",
                "Diaspora Consultation",
                "Partnership Proposal",
                "Other",
            ],
            "message_label": "Your Message",
            "message_placeholder": "Tell us about your project...",
            "submit_text": "Send Message",
        },
        "info": {
            "title": "Contact Information",
            "items": [
                {
                    "label": "Call Us",
                    "value": "+254 712 345 678",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-phone w-5 h-5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>""",
                },
                {
                    "label": "Email Us",
                    "value": "info@trustbuildurban.co.ke",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-mail w-5 h-5"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/></svg>""",
                },
                {
                    "label": "Visit Us",
                    "value": "Riverside Square, Riverside Dr,<br>Nairobi, Kenya",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-map-pin w-5 h-5"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>""",
                },
            ],
            "map": {
                "image_url": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&q=80&w=1200",
                "alt_text": "Office Location Map",
                "label": "Office Location",
            },
        },
    }

    context = {
        "meta": meta,
        "contact_header": contact_header,
        "contact_content": contact_content,
    }

    return render(request, "contact/contact.html", context)
