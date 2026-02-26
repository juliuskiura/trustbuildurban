from django.contrib import admin
from .models import ContactPage, ContactHeader, ContactContentSection, ContactSubmission


# class ContactHeaderInline(admin.StackedInline):
#     model = ContactHeader
#     can_delete = False
#     fk_name = 'contact_page'
#     extra = 0


# class ContactContentSectionInline(admin.StackedInline):
#     model = ContactContentSection
#     can_delete = False
#     fk_name = 'contact_page'
#     extra = 0


# class ContactPageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'status')
#     inlines = [ContactHeaderInline, ContactContentSectionInline]


# class ContactSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'email', 'subject', 'created_at', 'is_read')
#     list_filter = ('subject', 'created_at', 'is_read')
#     search_fields = ('first_name', 'last_name', 'email', 'message')
#     readonly_fields = ('created_at',)
#     ordering = ('-created_at',)


# admin.site.register(ContactPage, ContactPageAdmin)
# admin.site.register(ContactSubmission, ContactSubmissionAdmin)
