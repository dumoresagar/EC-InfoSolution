"""
Views for analytics app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import UserActivity
from .serializers import (
    UserActivitySerializer,
    ActivityCreateSerializer,
    AnalyticsSummarySerializer,
    TrendingDataSerializer,
    UserEngagementSerializer
)
from users.models import User
from recommendations.models import Recommendation


@method_decorator(ratelimit(key='ip', rate='20/m', method='POST'), name='create')
class UserActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user activity tracking.
    
    Endpoints:
    - POST /activity/ - Record user activity
    - GET /activity/ - List activities
    """
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ActivityCreateSerializer
        return UserActivitySerializer
    
    def create(self, request, *args, **kwargs):
        """Record a user activity."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()
        
        response_serializer = UserActivitySerializer(activity)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@ratelimit(key='ip', rate='30/m', method='GET')
def analytics_summary(request):
    """
    GET /analytics/summary/
    
    Return overall usage and engagement stats.
    """
    total_users = User.objects.count()
    total_activities = UserActivity.objects.count()
    total_recommendations = Recommendation.objects.count()
    
    # Activities by action type
    activities_by_action = {}
    action_counts = UserActivity.objects.values('action').annotate(count=Count('action'))
    for item in action_counts:
        activities_by_action[item['action']] = item['count']
    
    # Most active users
    most_active = UserActivity.objects.values('user__email', 'user__id') \
        .annotate(activity_count=Count('id')) \
        .order_by('-activity_count')[:10]
    
    most_active_users = [
        {
            'user_id': item['user__id'],
            'email': item['user__email'],
            'activity_count': item['activity_count']
        }
        for item in most_active
    ]
    
    data = {
        'total_users': total_users,
        'total_activities': total_activities,
        'total_recommendations': total_recommendations,
        'activities_by_action': activities_by_action,
        'most_active_users': most_active_users
    }
    
    return Response(data)


@api_view(['GET'])
@ratelimit(key='ip', rate='30/m', method='GET')
def analytics_trends(request):
    """
    GET /analytics/trends/
    
    Return trending genres and artists across all users.
    """
    # Get trending artists from activities
    trending_artists_data = UserActivity.objects.values('artist_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]
    
    trending_artists = [
        {'name': item['artist_name'], 'activity_count': item['count']}
        for item in trending_artists_data
    ]
    
    # Get popular tracks
    popular_tracks_data = UserActivity.objects.filter(action__in=['play', 'like']) \
        .values('track_id', 'track_name', 'artist_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]
    
    popular_tracks = [
        {
            'track_id': item['track_id'],
            'track_name': item['track_name'],
            'artist_name': item['artist_name'],
            'play_count': item['count']
        }
        for item in popular_tracks_data
    ]
    
    # Get trending genres from user profiles
    trending_genres = []
    all_genres = []
    users = User.objects.all()
    for user in users:
        try:
            all_genres.extend(user.profile.favorite_genres)
        except:
            pass
    
    if all_genres:
        from collections import Counter
        genre_counts = Counter(all_genres)
        trending_genres = [
            {'name': genre, 'count': count}
            for genre, count in genre_counts.most_common(10)
        ]
    
    data = {
        'trending_genres': trending_genres,
        'trending_artists': trending_artists,
        'popular_tracks': popular_tracks
    }
    
    return Response(data)


@api_view(['GET'])
@ratelimit(key='ip', rate='30/m', method='GET')
def user_engagement(request, user_id):
    """
    GET /analytics/user/{user_id}/
    
    Return user-specific engagement summary.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    total_activities = UserActivity.objects.filter(user=user).count()
    
    # Activities by action
    activities_by_action = {}
    action_counts = UserActivity.objects.filter(user=user) \
        .values('action').annotate(count=Count('action'))
    for item in action_counts:
        activities_by_action[item['action']] = item['count']
    
    # Favorite artists
    favorite_artists_data = UserActivity.objects.filter(user=user) \
        .values('artist_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    
    favorite_artists = [
        {'name': item['artist_name'], 'count': item['count']}
        for item in favorite_artists_data
    ]
    
    # Favorite tracks
    favorite_tracks_data = UserActivity.objects.filter(user=user) \
        .values('track_id', 'track_name', 'artist_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    
    favorite_tracks = [
        {
            'track_id': item['track_id'],
            'track_name': item['track_name'],
            'artist_name': item['artist_name'],
            'count': item['count']
        }
        for item in favorite_tracks_data
    ]
    
    # Recent activities
    recent_activities = UserActivity.objects.filter(user=user).order_by('-timestamp')[:10]
    recent_activities_serializer = UserActivitySerializer(recent_activities, many=True)
    
    data = {
        'user_id': user_id,
        'total_activities': total_activities,
        'activities_by_action': activities_by_action,
        'favorite_artists': favorite_artists,
        'favorite_tracks': favorite_tracks,
        'recent_activities': recent_activities_serializer.data
    }
    
    return Response(data)
