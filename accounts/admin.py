from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import UserAccount

class UserAccountAdmin(BaseUserAdmin):
    readonly_fields = ("signup_date",)
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_admin")
    ordering = ("signup_date",)
    list_display = ("username", "email", "first_name", "last_name", "signup_date", "is_staff", "is_active", "is_admin")
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'signup_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(UserAccount, UserAccountAdmin)

# Unregister the original Group admin
admin.site.unregister(Group)

class CustomGroupAdmin(GroupAdmin):
    search_fields = ("name",)
    list_display = ("name",)
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Permissions', {'fields': ('permissions',)}),
    )
    
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'permissions':
            kwargs['queryset'] = Permission.objects.all().select_related('content_type')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Register the new Group admin
admin.site.register(Group, CustomGroupAdmin)

