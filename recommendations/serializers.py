"""
Serializers for recommendations app.
"""
from rest_framework import serializers
from .models import Recommendation, RecommendationLog


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model."""
    
    class Meta:
        model = Recommendation
        fields = [
            'id',
            'track_id',
            'track_name',
            'artist_name',
            'album_name',
            'preview_url',
            'spotify_url',
            'album_art_url',
            'duration_ms',
            'popularity',
            'metadata',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RecommendationLogSerializer(serializers.ModelSerializer):
    """Serializer for RecommendationLog model."""
    
    class Meta:
        model = RecommendationLog
        fields = [
            'id',
            'user',
            'fetch_timestamp',
            'recommendations_count',
            'source',
            'status',
            'error_message',
            'metadata'
        ]
        read_only_fields = ['id', 'fetch_timestamp']


class RefreshRecommendationsSerializer(serializers.Serializer):
    """Serializer for triggering recommendation refresh."""
    limit = serializers.IntegerField(default=20, min_value=1, max_value=50)
    seed_genres = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        allow_empty=True
    )
    seed_artists = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        allow_empty=True
    )
