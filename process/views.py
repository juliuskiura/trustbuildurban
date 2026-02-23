from django.shortcuts import render

from process.models import ProcessPage, HeaderSection, ProcessSteps, ProcessCTA


def process(request):
    """Render the process page"""
    # Get the process page
    process_page = ProcessPage.objects.filter(is_published=True).first()

    if not process_page:
        # Fallback to basic context if no published page
        return render(
            request,
            "process/process.html",
            {
                "meta": {
                    "title": "Our Process | TrustBuild Urban",
                    "description": "Discover our 7-step roadmap to predictable construction results in Kenya.",
                }
            },
        )

    # Get sections
    header_section = getattr(process_page, "process_header", None)
    steps_section = process_page.process_steps_sections.first()
    cta_section = process_page.process_cta_sections.first()

    # Build context from database
    context = {
        "meta": {
            "title": process_page.meta_title or "Our Process | TrustBuild Urban",
            "description": process_page.meta_description
            or "Discover our 7-step roadmap to predictable construction results in Kenya.",
        }
    }

    # Header section context
    if header_section:
        context["process_header"] = {
            "eyebrow": header_section.eyebrow,
            "heading": header_section.heading,
            "description": header_section.description,
        }

    # Steps section context
    if steps_section:
        steps = []
        for step in steps_section.steps.all():
            steps.append(
                {
                    "title": step.title,
                    "description": step.description,
                }
            )

        context["process_steps"] = {
            "quality_gate_label": steps_section.quality_gate_label,
            "quality_gate_text": steps_section.quality_gate_text,
            "steps": steps,
        }

    # CTA section context
    if cta_section:
        context["process_cta"] = {
            "heading": cta_section.heading,
            "button_text": cta_section.button_text,
        }

    return render(request, "process/process.html", context)
