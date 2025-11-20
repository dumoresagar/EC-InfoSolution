"""
Admin configuration for recommendations app.
"""
from django.contrib import admin
from .models import Recommendation, RecommendationLog


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """Admin configuration for Recommendation model."""
    list_display = ('track_name', 'artist_name', 'user', 'popularity', 'created_at')
    list_filter = ('created_at', 'popularity')
    search_fields = ('track_name', 'artist_name', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    """Admin configuration for RecommendationLog model."""
    list_display = ('user', 'fetch_timestamp', 'recommendations_count', 'source', 'status')
    list_filter = ('status', 'source', 'fetch_timestamp')
    search_fields = ('user__email',)
    ordering = ('-fetch_timestamp',)
    readonly_fields = ('fetch_timestamp',)
