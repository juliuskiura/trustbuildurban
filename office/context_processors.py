from .models import Company


def company(request):
    """
    Inject the primary Company record into every template context.

    Available template variables:
        {{ company.trading_name }}   → "AnchorFields Ltd"
        {{ company.name }}           → "AnchorFields Limited"
        {{ company.tagline }}
        {{ company.primary_phone }}
        {{ company.primary_email }}
        {{ company.physical_address }}
        {{ company.city }}
        {{ company.po_box }}
        {{ company.website }}
        {{ company.facebook_url }}   (and other social URLs)
        {{ company.osm_embed_url }}  → OSM iframe src
        {{ company.osm_full_url }}   → full OSM link
    """
    try:
        co = Company.objects.first()
    except Exception:
        co = None
    return {"company": co}
