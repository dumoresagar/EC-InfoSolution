"""
Admin configuration for analytics app.
"""
from django.contrib import admin
from .models import UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin configuration for UserActivity model."""
    list_display = ('user', 'track_name', 'artist_name', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'track_name', 'artist_name')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
