from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "display_name", "is_staff"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Perfil", {"fields": ("display_name", "following")}),
    )
