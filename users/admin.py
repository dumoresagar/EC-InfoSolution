"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
