"""
Serializers for analytics app.
"""
from rest_framework import serializers
from .models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for UserActivity model."""
    
    class Meta:
        model = UserActivity
        fields = [
            'id',
            'user',
            'recommendation',
            'track_id',
            'track_name',
            'artist_name',
            'action',
            'timestamp',
            'metadata'
        ]
        read_only_fields = ['id', 'timestamp']


class ActivityCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating user activity."""
    
    class Meta:
        model = UserActivity
        fields = [
            'user',
            'recommendation',
            'track_id',
            'track_name',
            'artist_name',
            'action',
            'metadata'
        ]


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary data."""
    total_users = serializers.IntegerField()
    total_activities = serializers.IntegerField()
    total_recommendations = serializers.IntegerField()
    activities_by_action = serializers.DictField()
    most_active_users = serializers.ListField()


class TrendingDataSerializer(serializers.Serializer):
    """Serializer for trending genres and artists."""
    trending_genres = serializers.ListField()
    trending_artists = serializers.ListField()
    popular_tracks = serializers.ListField()


class UserEngagementSerializer(serializers.Serializer):
    """Serializer for user-specific engagement metrics."""
    user_id = serializers.IntegerField()
    total_activities = serializers.IntegerField()
    activities_by_action = serializers.DictField()
    favorite_artists = serializers.ListField()
    favorite_tracks = serializers.ListField()
    recent_activities = UserActivitySerializer(many=True)
