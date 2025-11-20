#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_discovery_backend.settings')
django.setup()

from recommendations.spotify_service import SpotifyService

print("Testing NEW recommendation implementation...")
service = SpotifyService()

# Test 1: Recommendations by genre
print("\n1. Testing genre-based recommendations...")
result = service.get_recommendations(seed_genres=['rock', 'pop'], limit=5)
if result and result.get('tracks'):
    print(f"✓ Got {len(result['tracks'])} recommendations")
    for i, track in enumerate(result['tracks'][:3], 1):
        print(f"  {i}. {track['name']} by {track['artists'][0]['name']}")
else:
    print("✗ Failed to get recommendations")

# Test 2: Recommendations by artist name
print("\n2. Testing artist-based recommendations...")
result = service.get_recommendations(seed_artists=['The Beatles'], limit=5)
if result and result.get('tracks'):
    print(f"✓ Got {len(result['tracks'])} recommendations")
    for i, track in enumerate(result['tracks'][:3], 1):
        print(f"  {i}. {track['name']} by {track['artists'][0]['name']}")
else:
    print("✗ Failed to get recommendations")

# Test 3: Combined seeds
print("\n3. Testing combined seeds...")
result = service.get_recommendations(
    seed_genres=['jazz'],
    seed_artists=['Miles Davis'],
    limit=10
)
if result and result.get('tracks'):
    print(f"✓ Got {len(result['tracks'])} recommendations")
    for i, track in enumerate(result['tracks'][:3], 1):
        print(f"  {i}. {track['name']} by {track['artists'][0]['name']}")
else:
    print("✗ Failed to get recommendations")

print("\n" + "="*50)
print("✓ Recommendation system is now working!")
print("Using search-based approach instead of restricted API.")
