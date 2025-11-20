"""
Spotify API integration service.
"""
import requests
import base64
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class SpotifyService:
    """
    Service class for interacting with Spotify Web API.
    """
    BASE_URL = 'https://api.spotify.com/v1'
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self._access_token = None
    
    def _get_access_token(self):
        """
        Get access token using client credentials flow.
        Cache the token for its lifetime.
        """
        cached_token = cache.get('spotify_access_token')
        if cached_token:
            return cached_token
        
        # Encode credentials
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {'grant_type': 'client_credentials'}
        
        try:
            response = requests.post(self.AUTH_URL, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600)
            
            # Cache the token for its lifetime minus 5 minutes for safety
            cache.set('spotify_access_token', access_token, expires_in - 300)
            
            return access_token
        except requests.RequestException as e:
            logger.error(f"Error getting Spotify access token: {str(e)}")
            raise
    
    def _get_headers(self):
        """Get headers with authorization token."""
        token = self._get_access_token()
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def search_tracks(self, query, limit=20):
        """
        Search for tracks on Spotify.
        """
        url = f"{self.BASE_URL}/search"
        params = {
            'q': query,
            'type': 'track',
            'limit': limit
        }
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error searching tracks: {str(e)}")
            return None
    
    def get_recommendations(self, seed_genres=None, seed_artists=None, seed_tracks=None, 
                          limit=20, **kwargs):
        """
        Get recommendations from Spotify using search-based approach.
        
        Note: Spotify's Recommendations API is restricted for new apps.
        This method uses search and artist's top tracks as an alternative.
        
        Args:
            seed_genres: List of genre seeds
            seed_artists: List of artist names or IDs
            seed_tracks: List of track IDs (optional)
            limit: Number of recommendations to get
            **kwargs: Additional parameters (ignored in this implementation)
        """
        recommendations = []
        
        try:
            # Strategy 1: Search by genres
            if seed_genres:
                for genre in seed_genres[:3]:
                    query = f"genre:{genre}"
                    tracks = self._search_tracks_for_recommendations(query, limit=limit//len(seed_genres[:3]))
                    recommendations.extend(tracks)
            
            # Strategy 2: Get artist's top tracks and related artists
            if seed_artists:
                for artist_identifier in seed_artists[:2]:
                    # Check if it's an artist ID or name
                    if len(artist_identifier) == 22:  # Spotify ID length
                        artist_id = artist_identifier
                    else:
                        # Search for artist by name
                        artist_result = self.search_artists(artist_identifier, limit=1)
                        if artist_result and artist_result.get('artists', {}).get('items'):
                            artist_id = artist_result['artists']['items'][0]['id']
                        else:
                            continue
                    
                    # Get artist's top tracks
                    top_tracks = self.get_artist_top_tracks(artist_id)
                    if top_tracks:
                        recommendations.extend(top_tracks[:limit//len(seed_artists[:2])])
                    
                    # Also search for similar artists by genre (related-artists endpoint is restricted)
                    artist_info = self.get_artist(artist_id)
                    if artist_info and artist_info.get('genres'):
                        genre = artist_info['genres'][0] if artist_info['genres'] else None
                        if genre:
                            similar_tracks = self._search_tracks_for_recommendations(
                                f"genre:{genre}",
                                limit=3
                            )
                            recommendations.extend(similar_tracks)
            
            # Strategy 3: Use seed tracks to find similar
            if seed_tracks:
                for track_id in seed_tracks[:2]:
                    track = self.get_track(track_id)
                    if track:
                        # Search for similar tracks by artist and genre
                        artist_name = track['artists'][0]['name']
                        similar = self._search_tracks_for_recommendations(
                            f"artist:{artist_name}", 
                            limit=3
                        )
                        recommendations.extend(similar)
            
            # If no seeds provided, get popular tracks
            if not recommendations:
                recommendations = self._search_tracks_for_recommendations("year:2023-2025", limit=limit)
            
            # Remove duplicates and limit
            seen = set()
            unique_recommendations = []
            for track in recommendations:
                if track['id'] not in seen:
                    seen.add(track['id'])
                    unique_recommendations.append(track)
                    if len(unique_recommendations) >= limit:
                        break
            
            return {
                'tracks': unique_recommendations[:limit]
            }
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return None
    
    def _search_tracks_for_recommendations(self, query, limit=10):
        """Helper method to search and format tracks for recommendations."""
        result = self.search_tracks(query, limit=limit)
        if result and result.get('tracks', {}).get('items'):
            return result['tracks']['items']
        return []
    
    def get_artist_top_tracks(self, artist_id, market='US'):
        """Get an artist's top tracks."""
        url = f"{self.BASE_URL}/artists/{artist_id}/top-tracks"
        params = {'market': market}
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('tracks', [])
        except requests.RequestException as e:
            logger.error(f"Error getting artist top tracks: {str(e)}")
            return []
    
    def get_related_artists(self, artist_id):
        """Get artists related to a given artist."""
        url = f"{self.BASE_URL}/artists/{artist_id}/related-artists"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            return data.get('artists', [])[:5]
        except requests.RequestException as e:
            logger.error(f"Error getting related artists: {str(e)}")
            return []
    
    def get_available_genre_seeds(self):
        """
        Get list of available genre seeds.
        """
        url = f"{self.BASE_URL}/recommendations/available-genre-seeds"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json().get('genres', [])
        except requests.RequestException as e:
            logger.error(f"Error getting genre seeds: {str(e)}")
            return []
    
    def search_artists(self, query, limit=10):
        """
        Search for artists on Spotify.
        """
        url = f"{self.BASE_URL}/search"
        params = {
            'q': query,
            'type': 'artist',
            'limit': limit
        }
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error searching artists: {str(e)}")
            return None
    
    def get_artist(self, artist_id):
        """
        Get artist details by ID.
        """
        url = f"{self.BASE_URL}/artists/{artist_id}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting artist: {str(e)}")
            return None
    
    def get_track(self, track_id):
        """
        Get track details by ID.
        """
        url = f"{self.BASE_URL}/tracks/{track_id}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting track: {str(e)}")
            return None
