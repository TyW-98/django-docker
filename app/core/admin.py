"""
Django Admin Dashboard Customisation
"""
from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    """Define custom user admin page layout""" # noqa
    ordering = ["id"]
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff"]
    
admin.site.register(models.CustomUser, CustomUserAdmin)