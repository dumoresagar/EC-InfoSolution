"""
Recommendation models for storing Spotify recommendations.
"""
from django.db import models
from users.models import User


class Recommendation(models.Model):
    """
    Store user recommendations from Spotify.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    track_id = models.CharField(max_length=255)
    track_name = models.CharField(max_length=500)
    artist_name = models.CharField(max_length=500)
    album_name = models.CharField(max_length=500, blank=True)
    preview_url = models.URLField(blank=True, null=True)
    spotify_url = models.URLField()
    album_art_url = models.URLField(blank=True, null=True)
    duration_ms = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['track_id']),
        ]

    def __str__(self):
        return f"{self.track_name} by {self.artist_name}"


class RecommendationLog(models.Model):
    """
    Log of recommendation fetch operations.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_logs')
    fetch_timestamp = models.DateTimeField(auto_now_add=True)
    recommendations_count = models.IntegerField(default=0)
    source = models.CharField(max_length=50, default='spotify')
    status = models.CharField(max_length=20, default='success')
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-fetch_timestamp']

    def __str__(self):
        return f"Log for {self.user.email} at {self.fetch_timestamp}"
