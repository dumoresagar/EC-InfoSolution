# Fixed API Endpoints

## Issue Resolution
The URL routing has been fixed. The endpoints now use `/user/{user_id}/` pattern to avoid conflicts with the router.

## Updated Endpoints

### User Recommendations

**Get recommendations for a user:**
```
GET http://127.0.0.1:8000/api/recommendations/user/{user_id}/
```

**Refresh recommendations:**
```
POST http://127.0.0.1:8000/api/recommendations/user/{user_id}/refresh/
Content-Type: application/json

{
  "limit": 20,
  "seed_genres": ["rock", "pop"],
  "seed_artists": ["The Beatles"]
}
```

### Quick Test Commands

**Test getting recommendations:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/recommendations/user/2/" -Method GET
```

**Test refreshing recommendations:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/recommendations/user/2/refresh/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"limit":20,"seed_genres":["rock","jazz"],"seed_artists":["Miles Davis"]}'
```

**Check Celery logs for task processing:**
```powershell
docker-compose logs -f celery
```

## All Working Endpoints

1. **User Management:**
   - `POST /api/users/` - Create user
   - `GET /api/users/{id}/` - Get user profile
   - `PUT/PATCH /api/users/{id}/` - Update user

2. **Recommendations:**
   - `GET /api/recommendations/user/{user_id}/` - Get recommendations ✅ FIXED
   - `POST /api/recommendations/user/{user_id}/refresh/` - Refresh recommendations ✅ FIXED
   - `GET /api/recommendations/list/` - List all recommendations (admin)

3. **Analytics:**
   - `POST /api/analytics/activity/` - Record activity
   - `GET /api/analytics/summary/` - Get summary
   - `GET /api/analytics/trends/` - Get trends
   - `GET /api/analytics/user/{user_id}/` - Get user engagement

## Admin Panel
- **URL:** http://127.0.0.1:8000/admin/
- **Static files:** ✅ Working (WhiteNoise configured)

## Notes
- All endpoints are working correctly
- Recommendations are being fetched from Spotify successfully
- Static files for admin panel are properly served
- API uses search-based recommendations (Spotify Recommendations API is restricted)
