#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_discovery_backend.settings')
django.setup()

from recommendations.spotify_service import SpotifyService
import requests

print("Testing Spotify API with different endpoints...")
service = SpotifyService()
headers = service._get_headers()

# Test different endpoints to find which ones work
endpoints = [
    ('Search Track', 'https://api.spotify.com/v1/search?q=rock&type=track&limit=1'),
    ('Search Artist', 'https://api.spotify.com/v1/search?q=Beatles&type=artist&limit=1'),
    ('Get Track', 'https://api.spotify.com/v1/tracks/11dFghVXANMlKmJXsNCbNl'),  # Popular track
    ('Get Artist', 'https://api.spotify.com/v1/artists/3WrFJ7ztbogyGnTHbHJFl2'),  # The Beatles
    ('Available Genres', 'https://api.spotify.com/v1/recommendations/available-genre-seeds'),
    ('Recommendations', 'https://api.spotify.com/v1/recommendations?seed_artists=3WrFJ7ztbogyGnTHbHJFl2&limit=1'),
]

for name, url in endpoints:
    print(f"\nTesting: {name}")
    print(f"URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ SUCCESS")
        else:
            print(f"✗ FAILED: {response.text[:100]}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

print("\n" + "="*50)
print("DIAGNOSIS:")
print("If search/track/artist endpoints work but recommendations don't,")
print("your Spotify app may not have the necessary permissions or")
print("the app is in Development Mode with restrictions.")
print("\nSolution: Go to https://developer.spotify.com/dashboard")
print("and check your app settings and quota.")
