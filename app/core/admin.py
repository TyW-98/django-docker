"""
Django Admin Dashboard Customisation
"""
from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as translate


class CustomUserAdmin(BaseUserAdmin):
    """Define custom user admin page layout""" # noqa
    ordering = ["id"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff"]
    fieldsets = (
        (translate("Login Credentials"), {"fields": ("email", "password")}),
        (translate("Permissions"), {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
        )}),
        (translate("Last active"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "email",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),
    )


admin.site.register(models.CustomUser, CustomUserAdmin)
