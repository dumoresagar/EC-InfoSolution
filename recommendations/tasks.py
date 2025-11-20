"""
Celery tasks for asynchronous recommendation fetching.
"""
from celery import shared_task
from django.core.cache import cache
from django.conf import settings
from .models import Recommendation, RecommendationLog
from .spotify_service import SpotifyService
from users.models import User
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def fetch_user_recommendations(self, user_id, limit=20, seed_genres=None, seed_artists=None):
    """
    Fetch recommendations for a specific user from Spotify API.
    
    Args:
        user_id: ID of the user
        limit: Number of recommendations to fetch
        seed_genres: List of genre seeds
        seed_artists: List of artist IDs
    """
    try:
        user = User.objects.get(id=user_id)
        spotify_service = SpotifyService()
        
        # Use user profile preferences if no seeds provided
        if not seed_genres and not seed_artists:
            try:
                profile = user.profile
                seed_genres = profile.favorite_genres[:5] if profile.favorite_genres else []
            except Exception as e:
                logger.warning(f"Could not get user profile: {str(e)}")
                seed_genres = ['pop', 'rock']  # Default genres
        
        # Fetch recommendations from Spotify
        recommendations_data = spotify_service.get_recommendations(
            seed_genres=seed_genres,
            seed_artists=seed_artists,
            limit=limit
        )
        
        if not recommendations_data or 'tracks' not in recommendations_data:
            raise Exception("Failed to fetch recommendations from Spotify")
        
        tracks = recommendations_data['tracks']
        
        # Clear old recommendations for this user (keep last 100)
        old_recommendations = Recommendation.objects.filter(user=user).order_by('-created_at')
        if old_recommendations.count() > 100:
            ids_to_keep = list(old_recommendations.values_list('id', flat=True)[:100])
            Recommendation.objects.filter(user=user).exclude(id__in=ids_to_keep).delete()
        
        # Save new recommendations
        created_count = 0
        for track in tracks:
            artists = ', '.join([artist['name'] for artist in track.get('artists', [])])
            album = track.get('album', {})
            images = album.get('images', [])
            
            Recommendation.objects.create(
                user=user,
                track_id=track['id'],
                track_name=track['name'],
                artist_name=artists,
                album_name=album.get('name', ''),
                preview_url=track.get('preview_url'),
                spotify_url=track['external_urls'].get('spotify', ''),
                album_art_url=images[0]['url'] if images else None,
                duration_ms=track.get('duration_ms', 0),
                popularity=track.get('popularity', 0),
                metadata={
                    'artists': track.get('artists', []),
                    'album': album,
                }
            )
            created_count += 1
        
        # Log the fetch operation
        RecommendationLog.objects.create(
            user=user,
            recommendations_count=created_count,
            source='spotify',
            status='success',
            metadata={
                'seed_genres': seed_genres,
                'seed_artists': seed_artists,
                'limit': limit
            }
        )
        
        # Cache the recommendations
        cache_key = f'user_recommendations_{user_id}'
        user_recommendations = Recommendation.objects.filter(user=user).order_by('-created_at')[:limit]
        cache.set(cache_key, list(user_recommendations.values()), settings.RECOMMENDATION_CACHE_TTL)
        
        logger.info(f"Successfully fetched {created_count} recommendations for user {user_id}")
        return {'status': 'success', 'count': created_count}
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {'status': 'error', 'message': 'User not found'}
    except Exception as e:
        logger.error(f"Error fetching recommendations for user {user_id}: {str(e)}")
        
        # Log the error
        try:
            user = User.objects.get(id=user_id)
            RecommendationLog.objects.create(
                user=user,
                recommendations_count=0,
                source='spotify',
                status='error',
                error_message=str(e)
            )
        except:
            pass
        
        # Retry the task
        raise self.retry(exc=e, countdown=60)


@shared_task
def refresh_all_user_recommendations():
    """
    Periodic task to refresh recommendations for all users.
    """
    users = User.objects.all()
    total_refreshed = 0
    
    for user in users:
        try:
            fetch_user_recommendations.delay(user.id)
            total_refreshed += 1
        except Exception as e:
            logger.error(f"Error queuing refresh for user {user.id}: {str(e)}")
    
    logger.info(f"Queued recommendation refresh for {total_refreshed} users")
    return {'status': 'success', 'users_queued': total_refreshed}
