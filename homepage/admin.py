from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import HomePage


@admin.register(HomePage)
class HomePageAdmin(MPTTModelAdmin):
    """
    Admin for HomePage model.
    """
    list_display = [
        'title', 
        'is_published', 
        'show_in_menus',
        'status',
        'updated_at'
    ]
    list_filter = [
        'is_published', 
        'show_in_menus',
        'created_at',
    ]
    search_fields = ['title', 'slug', 'seo_title', 'seo_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'revision_number',
    ]
    fieldsets = (
        ('Page Content', {
            'fields': (
                'parent',
                'title',
                'slug',
            )
        }),
        ('Hero Section', {
            'fields': (
                'hero_tagline',
                'hero_heading',
                'hero_description',
                'cta_primary_text',
                'cta_secondary_text',
            )
        }),
        ('Stats', {
            'fields': (
                'happy_customers_value',
                'property_sales_value',
                'award_winning_value',
            )
        }),
        ('Content', {
            'fields': (
                'introduction',
                'body',
            )
        }),
        ('SEO', {
            'fields': (
                'seo_title',
                'seo_description',
            ),
            'classes': ('collapse',)
        }),
        ('Navigation', {
            'fields': (
                'show_in_menus',
                'menu_order',
            )
        }),
        ('Publishing', {
            'fields': (
                'is_published',
                'published_date',
                'go_live_at',
                'expire_at',
            )
        }),
        ('Advanced', {
            'fields': (
                'custom_template',
                'created_by',
                'last_modified_by',
                'revision_number',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by', 'last_modified_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)
