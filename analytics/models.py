"""
Analytics models for tracking user activity and engagement.
"""
from django.db import models
from users.models import User
from recommendations.models import Recommendation


class UserActivity(models.Model):
    """
    Track user interactions with recommendations.
    """
    ACTION_CHOICES = [
        ('play', 'Play'),
        ('like', 'Like'),
        ('skip', 'Skip'),
        ('share', 'Share'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    recommendation = models.ForeignKey(
        Recommendation, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='activities'
    )
    track_id = models.CharField(max_length=255)
    track_name = models.CharField(max_length=500)
    artist_name = models.CharField(max_length=500)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['track_id']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.track_name}"
