# Architecture Migration Prompt for Django Apps

Use this prompt to migrate remaining Django apps (portfolio, services, blog, contact) from hardcoded data in views.py to database-driven models, following the established pattern from the homepage and about apps.

## Context

The project follows a consistent architectural pattern for database-driven content management:

### Base Pattern
```
Page Model (extends Page from pages/models.py)
├── Section Model(s) (OneToOne or ForeignKey)
│   ├── Section Header fields (eyebrow, heading, description, etc.)
│   └── Item Model(s) (ForeignKey with OrderedModel for ordering)
└── Additional Section Models needed
```

### Key Components

1. **Page asBase** from `core/models.py` - provides uuid, created_at, updated_at
2. **OrderedModel** from `ordered_model` package - provides drag-and-drop ordering
3. **GenericRelation** from `pages/models.py` Button model - for reusable buttons

## Example Pattern (from about app)

### Models Structure
```python
# about/models.py
from django.db import models
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel

class AboutPage(Page):
    """Inherits from Page, no extra fields needed"""
    class Meta:
        verbose_name = 'About Page'

    def get_template(self):
        return "about/about.html"

class HeroSection(PageBase):
    """OneToOne relationship with AboutPage"""
    about_page = models.OneToOneField(
        "about.AboutPage", 
        on_delete=models.CASCADE, 
        related_name="hero_section"
    )
    # Content fields
    eyebrow = models.CharField(max_length=100, blank=True, default="...")
    heading = models.CharField(max_length=200, blank=True, default="...")
    description = models.TextField(blank=True, default="...")
    # Image field (optional)
    image = models.ForeignKey("images.Image", on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    
class Stat(PageBase, OrderedModel):
    """Child model with ForeignKey and OrderedModel"""
    hero_section = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name="stats")
    value = models.CharField(max_length=20, blank=True)
    label = models.CharField(max_length=100, blank=True)
    order_with_respect_to = 'hero_section'
```

### Management Command Pattern
```python
# app/management/commands/populate_app_data.py
from django.core.management.base import BaseCommand
from django.db import transaction

from app.models import PageModel, SectionModel, ItemModel

class Command(BaseCommand):
    help = "Populate app sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show what would be created.")

    def handle(self, *args, **options):
        # Get or create Page
        page = PageModel.objects.filter(is_published=True).first()
        if not page:
            page = PageModel.objects.create(title="Page Title", slug="slug", is_published=True)
        
        # Data from views.py
        section_data = {...}
        
        if options.get("dry_run"):
            self._print_dry_run(page, section_data)
            return
            
        with transaction.atomic():
            # Create section
            section, created = SectionModel.objects.update_or_create(
                page=page,
                defaults={"field": section_data["field"]}
            )
            
            # Create items
            for idx, item_data in enumerate(section_data["items"]):
                item, created = ItemModel.objects.update_or_create(
                    section=section,
                    title=item_data["title"],
                    defaults={"description": item_data["description"], "order": idx + 1}
                )
        
        self.stdout.write(self.style.SUCCESS("Data population complete!"))
```

### Views Pattern
```python
# app/views.py
from django.shortcuts import render
from app.models import PageModel, SectionModel

def app_view(request):
    page = PageModel.objects.filter(is_published=True).first()
    
    if not page:
        return render(request, "app/template.html", {"meta": {...}})
    
    section = getattr(page, 'section_relation', None)
    
    context = {"meta": {"title": page.meta_title or "Default Title"}}
    
    if section:
        items = []
        for item in section.items.all():
            items.append({"title": item.title, "description": item.description})
        
        context["section"] = {
            "field": section.field,
            "items": items,
        }
    
    return render(request, "app/template.html", context)
```

### Admin Pattern
```python
# app/admin.py
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from app.models import PageModel, SectionModel, ItemModel

@admin.register(PageModel)
class PageModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published']

@admin.register(SectionModel)
class SectionModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'page', 'heading']
    raw_id_fields = ['page']

@admin.register(ItemModel)
class ItemModelAdmin(OrderedModelAdmin):
    list_display = ['__str__', 'section', 'order']
    list_filter = ['section']
```

## Steps to Apply

For each app (portfolio, services, blog, contact):

1. **Analyze views.py** - Identify hardcoded data structures (meta, sections, items)
2. **Analyze templates** - Understand expected context keys and structure
3. **Update models.py**:
   - Remove flat fields from Page model
   - Create Section models with ForeignKey/OneToOne
   - Create Item models with ForeignKey + OrderedModel
4. **Run migrations** - `python manage.py makemigrations app && python manage.py migrate`
5. **Create management command** - Follow populate pattern
6. **Run populate command** - `python manage.py populate_app_data`
7. **Update views.py** - Query database instead of hardcoded data
8. **Update admin.py** - Register all models
9. **Test** - Run `python manage.py check`

## Key Files Reference

- Homepage pattern: `homepage/models.py`, `homepage/management/commands/populate_homepage_data.py`
- About app pattern: `about/models.py`, `about/management/commands/populate_about_data.py`
- Process app pattern: `process/models.py`, `process/management/commands/populate_process_data.py`
- Base classes: `core/models.py` (PageBase), `pages/models.py` (Page, Button)
- Dependencies: `ordered_model` package for ordering
