from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    ProcessPage,
    HeaderSection,
    ProcessSteps,
    ProcessStep,
    ProcessCTA,
)


@admin.register(ProcessPage)
class ProcessPageAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title"]


@admin.register(HeaderSection)
class HeaderSectionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "process_page", "eyebrow", "heading"]
    raw_id_fields = ["process_page"]
    search_fields = ["process_page__title", "eyebrow", "heading"]


class ProcessStepInline(admin.TabularInline):
    model = ProcessStep
    extra = 1
    can_delete = True
    fieldsets = ((None, {"fields": ("title", "description", "order")}),)


@admin.register(ProcessSteps)
class ProcessStepsAdmin(admin.ModelAdmin):
    list_display = ["__str__", "process_page", "quality_gate_label"]
    raw_id_fields = ["process_page"]
    inlines = [ProcessStepInline]


@admin.register(ProcessStep)
class ProcessStepAdmin(OrderedModelAdmin):
    list_display = ["__str__", "process_steps", "title", "order"]
    list_filter = ["process_steps"]
    raw_id_fields = ["process_steps"]


@admin.register(ProcessCTA)
class ProcessCTAAdmin(admin.ModelAdmin):
    list_display = ["__str__", "process_page", "heading"]
    raw_id_fields = ["process_page"]
    search_fields = ["process_page__title", "heading"]
