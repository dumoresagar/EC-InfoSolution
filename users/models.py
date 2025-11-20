"""
User models for the music discovery backend.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    User profile with music preferences.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorite_genres = models.JSONField(default=list, blank=True)
    favorite_artists = models.JSONField(default=list, blank=True)
    moods = models.JSONField(default=list, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"
