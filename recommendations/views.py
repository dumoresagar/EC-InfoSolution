"""
Views for recommendations app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Recommendation, RecommendationLog
from .serializers import (
    RecommendationSerializer, 
    RecommendationLogSerializer,
    RefreshRecommendationsSerializer
)
from .tasks import fetch_user_recommendations
from users.models import User
import logging

logger = logging.getLogger(__name__)


@method_decorator(ratelimit(key='ip', rate='30/m'), name='list')
class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing recommendations.
    
    Endpoints:
    - GET /recommendations/ - List all recommendations
    - GET /recommendations/{id}/ - Get specific recommendation
    """
    serializer_class = RecommendationSerializer
    queryset = Recommendation.objects.all()


@api_view(['GET'])
@ratelimit(key='ip', rate='30/m', method='GET')
def get_user_recommendations(request, user_id):
    """
    GET /recommendations/{user_id}/
    
    Retrieve cached recommendations for a user.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Try to get from cache first
    cache_key = f'user_recommendations_{user_id}'
    cached_recommendations = cache.get(cache_key)
    
    if cached_recommendations:
        return Response({
            'user_id': user_id,
            'source': 'cache',
            'count': len(cached_recommendations),
            'recommendations': cached_recommendations
        })
    
    # If not in cache, get from database
    recommendations = Recommendation.objects.filter(user=user).order_by('-created_at')[:20]
    serializer = RecommendationSerializer(recommendations, many=True)
    
    # Cache the results
    cache.set(cache_key, serializer.data, settings.RECOMMENDATION_CACHE_TTL)
    
    return Response({
        'user_id': user_id,
        'source': 'database',
        'count': len(serializer.data),
        'recommendations': serializer.data
    })


@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', method='POST')
def refresh_user_recommendations(request, user_id):
    """
    POST /recommendations/{user_id}/refresh/
    
    Trigger asynchronous refresh of user recommendations.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = RefreshRecommendationsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    limit = data.get('limit', 20)
    seed_genres = data.get('seed_genres', None)
    seed_artists = data.get('seed_artists', None)
    
    # Queue the task
    task = fetch_user_recommendations.delay(
        user_id=user_id,
        limit=limit,
        seed_genres=seed_genres,
        seed_artists=seed_artists
    )
    
    return Response({
        'message': 'Recommendation refresh queued successfully',
        'user_id': user_id,
        'task_id': task.id,
        'status': 'pending'
    }, status=status.HTTP_202_ACCEPTED)
