from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UserAccount


class UserAccountAdmin(BaseUserAdmin):
    readonly_fields = ("signup_date", "reference")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_admin", "is_banned")
    ordering = ("signup_date",)
    list_display = ("username", "email", "first_name", "last_name", "signup_date", "is_staff", "is_active", "is_admin", "is_banned")
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'reference')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_admin', 'is_banned', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'signup_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'agree_terms'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(UserAccount, UserAccountAdmin)
