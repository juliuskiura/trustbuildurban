# About App Architecture Plan

## Executive Summary

This document outlines a comprehensive architecture plan to migrate the about app from hardcoded data in views.py to database-driven models, following the same architectural patterns established in the homepage app. The migration will ensure consistency across the project and enable content management through the Django admin interface.

---

## 1. Current State Analysis

### 1.1 Hardcoded Data in about/views.py

The current `about/views.py` contains the following hardcoded data structures:

#### Meta Information
```python
meta = {
    "title": "About | TrustBuild Urban",
    "description": "Learn about our mission of radical transparency and excellence in construction.",
}
```

#### Story Section (Hero)
```python
story_section = {
    "eyebrow": "Our Story",
    "heading": "Excellence in Construction, Built on Trust.",
    "description_1": "Founded on the principle of radical transparency...",
    "description_2": "Our mission is to provide a seamless...",
    "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a...",
    "image_alt": "Architecture Team",
    "quote": "Transparency isn't a buzzword; it's our core architecture.",
    "stats": {
        "years_experience": {"value": "10+", "label": "Years Experience"},
        "projects_completed": {"value": "150+", "label": "Projects Completed"},
    },
}
```

#### Core Pillars Section
```python
pillars_section = {
    "eyebrow": "The TrustBuild Standards",
    "heading": "Our Core Pillars",
    "pillars": [
        {
            "title": "Uncompromising Quality",
            "description": "We source premium materials...",
            "icon": "<svg>...</svg>",
        },
        {
            "title": "Client Partnership",
            "description": "We act as your local eyes...",
            "icon": "<svg>...</svg>",
        },
        {
            "title": "Ethical Conduct",
            "description": "From legal land acquisition...",
            "icon": "<svg>...</svg>",
        },
    ],
}
```

---

## 2. Homepage Pattern Analysis

### 2.1 Architectural Patterns Used

The homepage implementation follows these key patterns:

1. **Hierarchical Structure**: Page → Section → Items
2. **Base Classes**: Uses `PageBase` from `core.models` for timestamps and UUID
3. **Ordering**: Uses `OrderedModel` from `ordered_model` package for child items
4. **ForeignKey Relationships**: Parent-child relationships between models

### 2.2 Homepage Models Structure

```
HomePage (extends Page)
├── HeroSection (OneToOne)
│   └── Stats (ForeignKey, OrderedModel)
├── StatsSection (ForeignKey)
│   └── ClientReview (ForeignKey)
├── DiasporaSection (ForeignKey)
│   └── DiasporaChallenges (ForeignKey, OrderedModel)
├── FeaturesSection (ForeignKey)
│   └── Features (ForeignKey, OrderedModel)
├── StepsSection (ForeignKey)
│   └── Steps (ForeignKey, OrderedModel)
├── ServicesSection (ForeignKey)
│   └── Services (ForeignKey, OrderedModel)
└── NewsletterSection (ForeignKey)
```

---

## 3. Proposed About App Architecture

### 3.1 Data Entities Identified

| Entity | Type | Description |
|--------|------|-------------|
| AboutPage | Page | Main page model |
| HeroSection | Section | Hero/intro section with company story and image |
| Stat | Item | Individual stat items (years, projects) attached to HeroSection |
| CorePillarsSection | Section | Core values/pillars section |
| Pillar | Item | Individual pillar items (quality, partnership, ethics) |

### 3.2 Proposed Model Structure

```
AboutPage (extends Page)
├── HeroSection (OneToOne)
│   └── Stats (ForeignKey, OrderedModel)
└── CorePillarsSection (ForeignKey)
    └── Pillars (ForeignKey, OrderedModel)
```

---

## 4. Model Specifications

### 4.1 AboutPage Model

**File**: `about/models.py`

```python
class AboutPage(Page):
    """
    AboutPage model that inherits from the base Page model.
    This allows creating about page content from the admin panel.
    """
    
    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Pages'

    def get_template(self):
        """Use the existing about template"""
        return "about/about.html"

    def serve(self, request):
        """Serve the about page with additional context"""
        from django.shortcuts import render
        from .views import about
        return about(request)
```

> **Note**: The AboutPage model remains mostly unchanged.

### 4.2 HeroSection Model

**File**: `about/models.py`

```python
class HeroSection(PageBase):
    """
    Hero section model with OneToOne relationship to AboutPage.
    Contains the company story, hero image, and quote.
    """
    
    about_page = models.OneToOneField(
        "about.AboutPage", 
        on_delete=models.CASCADE, 
        related_name="hero_section"
    )
    
    # Section header
    eyebrow = models.CharField(max_length=100, blank=True, default="Our Story")
    heading = models.CharField(max_length=200, blank=True, 
        default="Excellence in Construction, Built on Trust.")
    
    # Description
    description = models.TextField(blank=True, 
        default="Founded on the principle of radical transparency, TrustBuild Urban has become the premier choice for Kenyans living abroad and local high-end homeowners. We recognized a massive gap in the market: the lack of corporate accountability in residential construction. Our mission is to provide a seamless, stress-free building experience where quality is never compromised, and every shilling is accounted for. We don't just build houses; we build legacies.")
    
    # Image - using ForeignKey to Image model (like homepage)
    image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="about_hero_sections",
    )
    image_url = models.URLField(max_length=500, blank=True)
    image_alt = models.CharField(max_length=200, blank=True, default="Architecture Team")
    
    # Quote
    quote = models.TextField(blank=True, 
        default="Transparency isn't a buzzword; it's our core architecture.")
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"Hero Section for {self.about_page.title}"
```

### 4.3 Stat Model

**File**: `about/models.py`

```python
class Stat(PageBase, OrderedModel):
    """
    Stat model with ForeignKey to HeroSection.
    Uses OrderedModel for ordering stats.
    Attached to HeroSection (not separate StatsSection like homepage).
    """
    
    hero_section = models.ForeignKey(
        HeroSection, 
        on_delete=models.CASCADE, 
        related_name="stats"
    )
    
    # Stat content
    value = models.CharField(max_length=20, blank=True)
    label = models.CharField(max_length=100, blank=True)
    
    # Order
    order_with_respect_to = 'hero_section'

    class Meta(OrderedModel.Meta):
        verbose_name = "Stat"
        verbose_name_plural = "Stats"

    def __str__(self):
        return f"{self.value} - {self.label}"
```

### 4.4 CorePillarsSection Model

**File**: `about/models.py`

```python
class CorePillarsSection(PageBase):
    """
    Core Pillars section model with ForeignKey to AboutPage.
    Contains core values and standards.
    """
    
    about_page = models.ForeignKey(
        "about.AboutPage", 
        on_delete=models.CASCADE, 
        related_name="core_pillars_sections"
    )
    
    # Section header
    eyebrow = models.CharField(max_length=100, blank=True, 
        default="The TrustBuild Standards")
    heading = models.CharField(max_length=200, blank=True, 
        default="Our Core Pillars")

    class Meta:
        verbose_name = "Core Pillars Section"
        verbose_name_plural = "Core Pillars Sections"

    def __str__(self):
        return f"Core Pillars Section for {self.about_page.title}"
```

### 4.5 Pillar Model

**File**: `about/models.py`

```python
class Pillar(PageBase, OrderedModel):
    """
    Pillar child model for CorePillarsSection.
    Uses OrderedModel for ordering pillars.
    """
    
    core_pillars_section = models.ForeignKey(
        CorePillarsSection, 
        on_delete=models.CASCADE, 
        related_name="pillars"
    )
    
    # Pillar content
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    icon = models.TextField(blank=True, help_text="SVG icon code")
    
    # Order
    order_with_respect_to = 'core_pillars_section'

    class Meta(OrderedModel.Meta):
        verbose_name = "Pillar"
        verbose_name_plural = "Pillars"

    def __str__(self):
        return self.title
```

---

## 5. Import Statements

The new `about/models.py` should include:

```python
from django.db import models
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel
```

---

## 6. Management Command Structure

### 6.1 Command Location

**File**: `about/management/commands/populate_about_data.py`

### 6.2 Command Structure

```python
"""
Management command to populate about page sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from about.models import (
    AboutPage,
    HeroSection,
    Stat,
    CorePillarsSection,
    Pillar,
)


class Command(BaseCommand):
    help = "Populate about page sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--about-id",
            type=int,
            help="ID of the AboutPage to populate data for. If not provided, will use the first published AboutPage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        about_id = options.get("about_id")
        dry_run = options.get("dry_run", False)

        # Get the AboutPage
        if about_id:
            try:
                about_page = AboutPage.objects.get(pk=about_id)
            except AboutPage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"AboutPage with ID {about_id} does not exist.")
                )
                return
        else:
            about_page = AboutPage.objects.filter(is_published=True).first()
            if not about_page:
                about_page = AboutPage.objects.first()
                if not about_page:
                    self.stderr.write(self.style.ERROR("No AboutPage found."))
                    return

        self.stdout.write(self.style.SUCCESS(f"Using AboutPage: {about_page.title} (ID: {about_page.pk})"))

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made."))

        # Data from views.py
        hero_section_data = {
            "eyebrow": "Our Story",
            "heading": "Excellence in Construction, Built on Trust.",
            "description": "Founded on the principle of radical transparency, TrustBuild Urban has become the premier choice for Kenyans living abroad and local high-end homeowners. We recognized a massive gap in the market: the lack of corporate accountability in residential construction. Our mission is to provide a seamless, stress-free building experience where quality is never compromised, and every shilling is accounted for. We don't just build houses; we build legacies.",
            "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a?auto=format&fit=crop&q=80&w=1200",
            "image_alt": "Architecture Team",
            "quote": "Transparency isn't a buzzword; it's our core architecture.",
            "stats": [
                {"value": "10+", "label": "Years Experience"},
                {"value": "150+", "label": "Projects Completed"},
            ],
        }

        pillars_section_data = {
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

        if dry_run:
            self._print_dry_run(about_page, hero_section_data, pillars_section_data)
            return

        # Create the sections
        with transaction.atomic():
            # 1. Create or Update Hero Section
            hero_section, created = HeroSection.objects.update_or_create(
                about_page=about_page,
                defaults={
                    "eyebrow": hero_section_data["eyebrow"],
                    "heading": hero_section_data["heading"],
                    "description": hero_section_data["description"],
                    "image_url": hero_section_data["image_url"],
                    "image_alt": hero_section_data["image_alt"],
                    "quote": hero_section_data["quote"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} HeroSection (ID: {hero_section.pk})"
                )
            )

            # Create Stats (attached to HeroSection)
            for idx, stat_data in enumerate(hero_section_data["stats"]):
                stat, created = Stat.objects.update_or_create(
                    hero_section=hero_section,
                    label=stat_data["label"],
                    defaults={
                        "value": stat_data["value"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Stat: {stat.label}"
                    )
                )

            # 2. Create or Update CorePillars Section
            pillars_section, created = CorePillarsSection.objects.update_or_create(
                about_page=about_page,
                defaults={
                    "eyebrow": pillars_section_data["eyebrow"],
                    "heading": pillars_section_data["heading"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} CorePillarsSection (ID: {pillars_section.pk})"
                )
            )

            # Create Pillars
            for idx, pillar_data in enumerate(pillars_section_data["pillars"]):
                pillar, created = Pillar.objects.update_or_create(
                    core_pillars_section=pillars_section,
                    title=pillar_data["title"],
                    defaults={
                        "description": pillar_data["description"],
                        "icon": pillar_data["icon"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Pillar: {pillar.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(self, about_page, hero_data, pillars_data):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"AboutPage: {about_page.title} (ID: {about_page.pk})\n")

        self.stdout.write("1. HeroSection:")
        self.stdout.write(f"   - eyebrow: {hero_data['eyebrow']}")
        self.stdout.write(f"   - heading: {hero_data['heading']}")
        self.stdout.write(f"   - quote: {hero_data['quote']}")
        self.stdout.write("   - Stats:")
        for stat in hero_data["stats"]:
            self.stdout.write(f"     * {stat['label']}: {stat['value']}")

        self.stdout.write("\n2. CorePillarsSection:")
        self.stdout.write(f"   - eyebrow: {pillars_data['eyebrow']}")
        self.stdout.write(f"   - heading: {pillars_data['heading']}")
        self.stdout.write("   - Pillars:")
        for pillar in pillars_data["pillars"]:
            self.stdout.write(f"     * {pillar['title']}")
```

---

## 7. Migration Plan

### 7.1 Step-by-Step Migration

1. **Create new models** in `about/models.py`
2. **Generate migrations**: `python manage.py makemigrations about`
3. **Run migrations**: `python manage.py migrate`
4. **Create management command**: `about/management/commands/populate_about_data.py`
5. **Run populate command**: `python manage.py populate_about_data`
6. **Update views.py** to query database instead of returning hardcoded data
7. **Update templates** if needed to use new model relationships
8. **Update admin.py** to register new models for admin management

### 7.2 Migration File Preview

The migration will create the following tables:

| Table | Description |
|-------|-------------|
| about_herosection | Hero section content |
| about_stat | Statistics (ordered, attached to HeroSection) |
| about_corepillarssection | Core pillars section content |
| about_pillar | Individual pillars (ordered) |

---

## 8. Views Update

### 8.1 Updated about/views.py

```python
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from about.models import AboutPage, HeroSection, CorePillarsSection


def about(request):
    """Render the about page"""
    # Get the about page
    about_page = AboutPage.objects.filter(is_published=True).first()
    
    if not about_page:
        # Fallback to basic context if no published page
        return render(request, "about/about.html", {
            'meta': {
                "title": "About | TrustBuild Urban",
                "description": "Learn about our mission of radical transparency and excellence in construction.",
            }
        })
    
    # Get sections
    hero_section = getattr(about_page, 'hero_section', None)
    pillars_section = about_page.core_pillars_sections.first()
    
    # Build context from database
    context = {
        "meta": {
            "title": about_page.meta_title or "About | TrustBuild Urban",
            "description": about_page.meta_description or "Learn about our mission of radical transparency and excellence in construction.",
        }
    }
    
    # Hero section context
    if hero_section:
        story_stats = {}
        for stat in hero_section.stats.all():
            if stat.label == "Years Experience":
                story_stats["years_experience"] = {"value": stat.value, "label": stat.label}
            elif stat.label == "Projects Completed":
                story_stats["projects_completed"] = {"value": stat.value, "label": stat.label}
        
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
            pillars.append({
                "title": pillar.title,
                "description": pillar.description,
                "icon": pillar.icon,
            })
        
        context["pillars_section"] = {
            "eyebrow": pillars_section.eyebrow,
            "heading": pillars_section.heading,
            "pillars": pillars,
        }
    
    return render(request, "about/about.html", context)
```

---

## 9. Admin Registration

### 9.1 Updated about/admin.py

```python
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import AboutPage, HeroSection, Stat, CorePillarsSection, Pillar


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at']
    list_filter = ['is_published']
    search_fields = ['title']


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['about_page', 'eyebrow', 'heading']
    raw_id_fields = ['about_page', 'image']


@admin.register(Stat)
class StatAdmin(OrderedModelAdmin):
    list_display = ['__str__', 'hero_section', 'order']
    list_filter = ['hero_section']


@admin.register(CorePillarsSection)
class CorePillarsSectionAdmin(admin.ModelAdmin):
    list_display = ['about_page', 'eyebrow', 'heading']
    raw_id_fields = ['about_page']


@admin.register(Pillar)
class PillarAdmin(OrderedModelAdmin):
    list_display = ['__str__', 'core_pillars_section', 'order']
    list_filter = ['core_pillars_section']
```

---

## 10. Consistency with Homepage

### 10.1 Pattern Compliance

| Pattern | Homepage | About App |
|---------|----------|-----------|
| Base class (PageBase) | ✓ | ✓ |
| OrderedModel for items | ✓ | ✓ |
| ForeignKey relationships | ✓ | ✓ |
| Section → Items structure | ✓ | ✓ |
| Stats attached to HeroSection | - | ✓ (as requested) |
| Management command | ✓ | ✓ |
| update_or_create pattern | ✓ | ✓ |
| transaction.atomic() | ✓ | ✓ |
| --dry-run option | ✓ | ✓ |

---

## 11. Implementation Checklist

- [ ] 1. Update `about/models.py` with new models
- [ ] 2. Create migration: `python manage.py makemigrations about`
- [ ] 3. Run migration: `python manage.py migrate`
- [ ] 4. Create management command directory structure
- [ ] 5. Create `populate_about_data.py` management command
- [ ] 6. Run populate command: `python manage.py populate_about_data`
- [ ] 7. Update `about/views.py` to query database
- [ ] 8. Update `about/admin.py` to register new models
- [ ] 9. Test the about page renders correctly
- [ ] 10. Verify admin interface for content management

---

## 12. Benefits of This Architecture

1. **Admin Control**: Content can be managed through Django admin without code changes
2. **Scalability**: Easy to add new sections or modify existing ones
3. **Consistency**: Follows established patterns from homepage
4. **Maintainability**: Clear separation of concerns
5. **Performance**: Database queries are more efficient than hardcoded data
6. **Reusability**: Models can be extended or reused in other apps

---

*Document Version: 1.1*  
*Created: 2026-02-23*  
*Based on: Homepage App Architecture Pattern*  
*Updated per user feedback: HeroSection with Stats via FK, CorePillarsSection with Pillars child model*
