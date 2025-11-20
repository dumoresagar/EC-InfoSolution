# Music Discovery Backend

A scalable backend service that provides music recommendations to users using data from the Spotify Web API. Built with Django, PostgreSQL, Redis, Celery, and Docker.

## 🎵 Features

- **User Management**: Create and manage user profiles with music preferences
- **Spotify Integration**: Fetch personalized music recommendations from Spotify Web API
- **Smart Caching**: Redis-based caching for optimized performance
- **Asynchronous Processing**: Celery-powered background tasks for recommendation updates
- **Analytics & Reporting**: Track user engagement and identify trending content
- **Rate Limiting**: Built-in API rate limiting for security
- **Containerized**: Full Docker setup for easy deployment

## 🏗️ Architecture

### Tech Stack
- **Backend Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery + Redis broker
- **Web Server**: Gunicorn + Nginx
- **Containerization**: Docker + Docker Compose

### Project Structure
```
music_discovery_backend/
├── users/                  # User management app
├── recommendations/        # Recommendation engine
├── analytics/             # Analytics & reporting
├── music_discovery_backend/  # Main project settings
├── docker-compose.yml     # Docker orchestration
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
├── Makefile             # Build automation
└── README.md           # This file
```

## 📋 API Endpoints

### Users
- `POST /api/users/` - Create user with preferences
- `GET /api/users/{user_id}/` - Retrieve user profile
- `PUT /api/users/{user_id}/` - Update user profile
- `DELETE /api/users/{user_id}/` - Delete user

### Recommendations
- `GET /api/recommendations/{user_id}/` - Get cached recommendations
- `POST /api/recommendations/{user_id}/refresh/` - Trigger async recommendation refresh

### Analytics
- `POST /api/analytics/activity/` - Record user activity (play, like, skip)
- `GET /api/analytics/summary/` - Overall engagement statistics
- `GET /api/analytics/trends/` - Trending genres and artists
- `GET /api/analytics/user/{user_id}/` - User-specific engagement metrics

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Spotify Developer Account (for API credentials)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd music_discovery_backend
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Spotify API credentials
# Get credentials from: https://developer.spotify.com/dashboard
```

### 3. Get Spotify API Credentials
1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy the Client ID and Client Secret
4. Add them to your `.env` file

### 4. Build and Run
Using the Makefile:
```bash
# Build and start all services
make setup

# Create a superuser for Django admin
make createsuperuser
```

Or using Docker Compose directly:
```bash
# Build the containers
docker-compose build

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the API
- API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

## 🔧 Development Commands

### Using Makefile
```bash
make help          # Show all available commands
make up            # Start services
make down          # Stop services
make logs          # View logs
make shell         # Open Django shell
make migrate       # Run migrations
make test          # Run tests
make clean         # Clean up containers and volumes
```

### Manual Commands
```bash
# View logs
docker-compose logs -f

# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Run tests
docker-compose exec web pytest

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📝 API Usage Examples

### 1. Create a User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "profile": {
      "favorite_genres": ["rock", "pop", "jazz"],
      "favorite_artists": ["The Beatles", "Queen"],
      "moods": ["happy", "energetic"]
    }
  }'
```

### 2. Get User Profile
```bash
curl http://localhost:8000/api/users/1/
```

### 3. Refresh Recommendations
```bash
curl -X POST http://localhost:8000/api/recommendations/1/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "limit": 20,
    "seed_genres": ["rock", "pop"]
  }'
```

### 4. Get Recommendations
```bash
curl http://localhost:8000/api/recommendations/1/
```

### 5. Record Activity
```bash
curl -X POST http://localhost:8000/api/analytics/activity/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "track_id": "3n3Ppam7vgaVa1iaRUc9Lp",
    "track_name": "Mr. Brightside",
    "artist_name": "The Killers",
    "action": "play"
  }'
```

### 6. Get Analytics
```bash
# Overall summary
curl http://localhost:8000/api/analytics/summary/

# Trending content
curl http://localhost:8000/api/analytics/trends/

# User engagement
curl http://localhost:8000/api/analytics/user/1/
```

## 🧪 Testing

The project includes unit tests for core functionality:

```bash
# Run all tests
make test

# Or manually
docker-compose exec web pytest

# Run specific test file
docker-compose exec web pytest users/tests.py
```

## 📦 Postman Collection

Import the `Music_Discovery_API.postman_collection.json` file into Postman for easy API testing.

## 🔐 Security Features

- **Rate Limiting**: Prevents API abuse with configurable rate limits
- **CORS Protection**: Configured CORS headers for secure cross-origin requests
- **Environment Variables**: Sensitive data stored in environment variables
- **Password Hashing**: Django's built-in password hashing
- **SQL Injection Protection**: ORM-based queries prevent SQL injection

## 📊 Database Schema

### User Model
- id, username, email, password (hashed)
- created_at, updated_at

### UserProfile Model
- user (FK), favorite_genres, favorite_artists, moods, preferences
- created_at, updated_at

### Recommendation Model
- user (FK), track_id, track_name, artist_name, album_name
- preview_url, spotify_url, album_art_url
- duration_ms, popularity, metadata
- created_at

### UserActivity Model
- user (FK), recommendation (FK), track_id, track_name, artist_name
- action (play/like/skip/share), timestamp, metadata

## ⚡ Performance Optimizations

1. **Redis Caching**: Recommendations cached for 1 hour
2. **Database Indexing**: Optimized queries with proper indexes
3. **Async Processing**: Heavy operations run in background
4. **Connection Pooling**: Efficient database connections
5. **Pagination**: Large result sets paginated automatically

## 🔄 Background Tasks

### Celery Tasks
- `fetch_user_recommendations`: Fetch Spotify recommendations for a user
- `refresh_all_user_recommendations`: Periodic refresh for all users (runs hourly)

View Celery logs:
```bash
docker-compose logs -f celery
```

## 🌐 Environment Variables

See `.env.example` for all configurable options:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (required) |
| `DEBUG` | Debug mode | False |
| `ALLOWED_HOSTS` | Allowed hosts | * |
| `POSTGRES_DB` | Database name | music_discovery_db |
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | postgres |
| `REDIS_HOST` | Redis host | redis |
| `SPOTIFY_CLIENT_ID` | Spotify Client ID | (required) |
| `SPOTIFY_CLIENT_SECRET` | Spotify Client Secret | (required) |

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Database Connection Issues
```bash
# Ensure PostgreSQL is healthy
docker-compose ps

# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

### Redis Connection Issues
```bash
# Check Redis status
docker-compose exec redis redis-cli ping

# Should return: PONG
```

## 📈 Future Enhancements

- [ ] User authentication with JWT tokens
- [ ] WebSocket support for real-time updates
- [ ] Machine learning-based recommendation engine
- [ ] Social features (follow users, share playlists)
- [ ] Advanced search and filtering
- [ ] Export recommendations to Spotify playlists
- [ ] Multi-language support
- [ ] Mobile app integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request



## 🙏 Acknowledgments

- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- Django and Django REST Framework communities
- All open-source contributors

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review Spotify API documentation

## ⚠️ Important Notes & Assumptions

### Assumptions
1. **Spotify API Access**: Requires valid Spotify Developer credentials
2. **Rate Limits**: Spotify API has rate limits - the service respects them
3. **Data Privacy**: User data is stored locally and not shared
4. **Scalability**: Designed for horizontal scaling with load balancers

### Limitations
1. **Spotify API Dependency**: Recommendations depend on Spotify API availability
2. **Genre Seeds**: Spotify API limits to 5 total seeds per request
3. **Authentication**: Basic authentication implemented (can be enhanced with OAuth)
4. **Recommendation Algorithm**: Uses Spotify's algorithm (no custom ML model)

### Production Considerations
1. Change `SECRET_KEY` to a secure random value
2. Set `DEBUG=False` in production
3. Configure proper `ALLOWED_HOSTS`
4. Use environment-specific `.env` files
5. Set up SSL/TLS certificates
6. Configure monitoring and logging
7. Implement backup strategies
8. Use managed database services for production

---

**Built with ❤️ for music lovers**
