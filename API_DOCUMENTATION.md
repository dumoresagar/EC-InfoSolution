# API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Table of Contents
- [User Management](#user-management)
- [Recommendations](#recommendations)
- [Analytics](#analytics)
- [Error Handling](#error-handling)

---

## User Management

### Create User
Create a new user with preferences.

**Endpoint:** `POST /api/users/`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "profile": {
    "favorite_genres": ["rock", "pop", "jazz"],
    "favorite_artists": ["The Beatles", "Queen", "Miles Davis"],
    "moods": ["happy", "energetic", "relaxed"],
    "preferences": {
      "language": "en",
      "explicit_content": false
    }
  }
}
```

**Response:** `201 CREATED`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile": {
    "favorite_genres": ["rock", "pop", "jazz"],
    "favorite_artists": ["The Beatles", "Queen", "Miles Davis"],
    "moods": ["happy", "energetic", "relaxed"],
    "preferences": {
      "language": "en",
      "explicit_content": false
    },
    "created_at": "2025-11-18T10:30:00Z",
    "updated_at": "2025-11-18T10:30:00Z"
  },
  "created_at": "2025-11-18T10:30:00Z",
  "updated_at": "2025-11-18T10:30:00Z"
}
```

### Get User Profile
Retrieve a user's profile and preferences.

**Endpoint:** `GET /api/users/{user_id}/`

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile": {
    "favorite_genres": ["rock", "pop", "jazz"],
    "favorite_artists": ["The Beatles", "Queen", "Miles Davis"],
    "moods": ["happy", "energetic", "relaxed"],
    "preferences": {
      "language": "en",
      "explicit_content": false
    },
    "created_at": "2025-11-18T10:30:00Z",
    "updated_at": "2025-11-18T10:30:00Z"
  },
  "created_at": "2025-11-18T10:30:00Z",
  "updated_at": "2025-11-18T10:30:00Z"
}
```

### Update User Profile
Update user information and preferences.

**Endpoint:** `PUT /api/users/{user_id}/` or `PATCH /api/users/{user_id}/`

**Request Body:**
```json
{
  "profile": {
    "favorite_genres": ["rock", "metal", "blues"],
    "moods": ["energetic", "focused"]
  }
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile": {
    "favorite_genres": ["rock", "metal", "blues"],
    "favorite_artists": ["The Beatles", "Queen", "Miles Davis"],
    "moods": ["energetic", "focused"],
    "preferences": {
      "language": "en",
      "explicit_content": false
    },
    "created_at": "2025-11-18T10:30:00Z",
    "updated_at": "2025-11-18T12:45:00Z"
  },
  "created_at": "2025-11-18T10:30:00Z",
  "updated_at": "2025-11-18T12:45:00Z"
}
```

---

## Recommendations

### Get User Recommendations
Retrieve cached recommendations for a user.

**Endpoint:** `GET /api/recommendations/user/{user_id}/`

**Response:** `200 OK`
```json
{
  "user_id": 1,
  "source": "cache",
  "count": 20,
  "recommendations": [
    {
      "id": 1,
      "track_id": "3n3Ppam7vgaVa1iaRUc9Lp",
      "track_name": "Mr. Brightside",
      "artist_name": "The Killers",
      "album_name": "Hot Fuss",
      "preview_url": "https://p.scdn.co/mp3-preview/...",
      "spotify_url": "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp",
      "album_art_url": "https://i.scdn.co/image/...",
      "duration_ms": 222973,
      "popularity": 87,
      "metadata": {
        "artists": [...],
        "album": {...}
      },
      "created_at": "2025-11-18T11:00:00Z"
    }
  ]
}
```

### Refresh Recommendations
Trigger asynchronous refresh of recommendations from Spotify.

**Endpoint:** `POST /api/recommendations/user/{user_id}/refresh/`

**Request Body:**
```json
{
  "limit": 20,
  "seed_genres": ["rock", "pop"],
  "seed_artists": ["4Z8W4fKeB5YxbusRsdQVPb"]
}
```

**Parameters:**
- `limit` (optional): Number of recommendations (1-50, default: 20)
- `seed_genres` (optional): List of genre seeds
- `seed_artists` (optional): List of Spotify artist IDs

**Response:** `202 ACCEPTED`
```json
{
  "message": "Recommendation refresh queued successfully",
  "user_id": 1,
  "task_id": "abc123-def456-ghi789",
  "status": "pending"
}
```

---

## Analytics

### Record User Activity
Track user interactions with songs.

**Endpoint:** `POST /api/analytics/activity/`

**Request Body:**
```json
{
  "user": 1,
  "track_id": "3n3Ppam7vgaVa1iaRUc9Lp",
  "track_name": "Mr. Brightside",
  "artist_name": "The Killers",
  "action": "play",
  "recommendation": 1,
  "metadata": {
    "duration_listened": 180000,
    "source": "recommendations"
  }
}
```

**Actions:**
- `play` - User played the track
- `like` - User liked the track
- `skip` - User skipped the track
- `share` - User shared the track

**Response:** `201 CREATED`
```json
{
  "id": 1,
  "user": 1,
  "recommendation": 1,
  "track_id": "3n3Ppam7vgaVa1iaRUc9Lp",
  "track_name": "Mr. Brightside",
  "artist_name": "The Killers",
  "action": "play",
  "timestamp": "2025-11-18T11:30:00Z",
  "metadata": {
    "duration_listened": 180000,
    "source": "recommendations"
  }
}
```

### Get Analytics Summary
Get overall platform statistics.

**Endpoint:** `GET /api/analytics/summary/`

**Response:** `200 OK`
```json
{
  "total_users": 150,
  "total_activities": 5420,
  "total_recommendations": 3000,
  "activities_by_action": {
    "play": 3200,
    "like": 1100,
    "skip": 980,
    "share": 140
  },
  "most_active_users": [
    {
      "user_id": 1,
      "email": "john@example.com",
      "activity_count": 234
    },
    {
      "user_id": 5,
      "email": "jane@example.com",
      "activity_count": 189
    }
  ]
}
```

### Get Trending Data
Get trending genres, artists, and tracks across all users.

**Endpoint:** `GET /api/analytics/trends/`

**Response:** `200 OK`
```json
{
  "trending_genres": [
    {
      "name": "rock",
      "count": 145
    },
    {
      "name": "pop",
      "count": 132
    }
  ],
  "trending_artists": [
    {
      "name": "The Killers",
      "activity_count": 89
    },
    {
      "name": "Queen",
      "activity_count": 76
    }
  ],
  "popular_tracks": [
    {
      "track_id": "3n3Ppam7vgaVa1iaRUc9Lp",
      "track_name": "Mr. Brightside",
      "artist_name": "The Killers",
      "play_count": 156
    }
  ]
}
```

### Get User Engagement
Get user-specific engagement metrics.

**Endpoint:** `GET /api/analytics/user/{user_id}/`

**Response:** `200 OK`
```json
{
  "user_id": 1,
  "total_activities": 234,
  "activities_by_action": {
    "play": 150,
    "like": 60,
    "skip": 20,
    "share": 4
  },
  "favorite_artists": [
    {
      "name": "The Killers",
      "count": 45
    },
    {
      "name": "Queen",
      "count": 32
    }
  ],
  "favorite_tracks": [
    {
      "track_id": "3n3Ppam7vgaVa1iaRUc9Lp",
      "track_name": "Mr. Brightside",
      "artist_name": "The Killers",
      "count": 23
    }
  ],
  "recent_activities": [
    {
      "id": 234,
      "track_name": "Mr. Brightside",
      "artist_name": "The Killers",
      "action": "play",
      "timestamp": "2025-11-18T14:30:00Z"
    }
  ]
}
```

---

## Error Handling

### Error Response Format
All errors follow a consistent format:

```json
{
  "error": "Error message describing what went wrong",
  "detail": "Additional details about the error (optional)"
}
```

### HTTP Status Codes

| Status Code | Meaning |
|-------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 202 | Accepted - Request accepted for processing |
| 400 | Bad Request - Invalid request data |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

### Rate Limiting

Rate limits are applied per IP address:

| Endpoint | Rate Limit |
|----------|-----------|
| POST /api/users/ | 10 requests/minute |
| GET /api/recommendations/ | 30 requests/minute |
| POST /api/recommendations/refresh/ | 5 requests/minute |
| POST /api/analytics/activity/ | 20 requests/minute |
| GET /api/analytics/* | 30 requests/minute |

**Rate Limit Error:**
```json
{
  "error": "Rate limit exceeded",
  "detail": "Too many requests. Please try again later."
}
```

---

## Examples

### Complete User Flow

#### 1. Create a user
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "music_lover",
    "email": "lover@example.com",
    "password": "secure123",
    "profile": {
      "favorite_genres": ["rock", "indie"],
      "moods": ["happy"]
    }
  }'
```

#### 2. Trigger recommendation refresh
```bash
curl -X POST http://localhost:8000/api/recommendations/user/1/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "limit": 20,
    "seed_genres": ["rock", "indie"]
  }'
```

#### 3. Get recommendations (wait a few seconds)
```bash
curl http://localhost:8000/api/recommendations/user/1/
```

#### 4. Record activity
```bash
curl -X POST http://localhost:8000/api/analytics/activity/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "track_id": "track_id_here",
    "track_name": "Song Name",
    "artist_name": "Artist Name",
    "action": "play"
  }'
```

#### 5. Check user engagement
```bash
curl http://localhost:8000/api/analytics/user/1/
```

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- Recommendations are cached for 1 hour
- Background tasks may take a few seconds to complete
- Spotify API credentials are required for recommendations
- Maximum 5 seed values total (genres + artists + tracks combined)
