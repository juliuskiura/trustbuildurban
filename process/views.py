from django.shortcuts import render


def process(request):
    """Render the process page"""
    # Meta information
    meta = {
        "title": "Our Process | TrustBuild Urban",
        "description": "Discover our 7-step roadmap to predictable construction results in Kenya.",
    }

    # Process header section
    process_header = {
        "eyebrow": "How We Work",
        "heading": "The 7-Step TrustBuild Roadmap",
        "description": "Construction in Kenya doesn't have to be chaotic. We use a standardized corporate workflow to ensure predictable results every time.",
    }

    # Process steps section
    process_steps = {
        "quality_gate_label": "Quality Gate",
        "quality_gate_text": "This stage must be signed off by both our lead engineer and the client before proceeding.",
        "steps": [
            {
                "title": "Consultation",
                "description": "Brainstorming and roadmap development.",
            },
            {
                "title": "Feasibility",
                "description": "Site visits and legal title verification.",
            },
            {
                "title": "Concept",
                "description": "Architectural designs and floor planning.",
            },
            {
                "title": "Approvals",
                "description": "NCA and County government legal sign-offs.",
            },
            {
                "title": "Contracts",
                "description": "Bill of quantities and fixed-price agreements.",
            },
            {
                "title": "Construction",
                "description": "Structured building with live video updates.",
            },
            {
                "title": "Handover",
                "description": "Quality verification and key ceremony.",
            },
        ],
    }

    # Process CTA section
    process_cta = {
        "heading": "Ready to take step one?",
        "button_text": "Book Initial Consultation",
    }

    context = {
        "meta": meta,
        "process_header": process_header,
        "process_steps": process_steps,
        "process_cta": process_cta,
    }

    return render(request, "process/process.html", context)
