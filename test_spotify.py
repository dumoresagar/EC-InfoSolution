#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_discovery_backend.settings')
django.setup()

from recommendations.spotify_service import SpotifyService
import requests

print("Testing Spotify API...")
service = SpotifyService()

# Test 1: Get access token
print("\n1. Testing access token...")
token = service._get_access_token()
print(f"✓ Token obtained: {token[:30]}...")

# Test 2: Get available genres
print("\n2. Testing available genre seeds endpoint...")
headers = service._get_headers()
response = requests.get('https://api.spotify.com/v1/recommendations/available-genre-seeds', headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Test 3: Try a simple recommendation
print("\n3. Testing recommendations with seed_genres...")
response = requests.get(
    'https://api.spotify.com/v1/recommendations',
    headers=headers,
    params={'seed_genres': 'pop', 'limit': 5}
)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✓ Got {len(data.get('tracks', []))} recommendations")
else:
    print(f"Error: {response.text}")

# Test 4: Check if the credentials have proper scopes
print("\n4. Checking API access...")
print(f"Client ID: {service.client_id[:10]}...")
print(f"Token type: Bearer")
