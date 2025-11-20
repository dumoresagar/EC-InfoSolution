# Quick Start Guide

Get the Music Discovery Backend up and running in 5 minutes!

## Prerequisites

✅ Docker Desktop installed and running  
✅ Spotify Developer Account (free)  
✅ Text editor for configuration  

## Step 1: Get Spotify API Credentials (2 minutes)

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **"Create App"**
3. Fill in:
   - **App name**: Music Discovery Backend
   - **App description**: Personal music recommendation service
   - **Redirect URI**: `http://localhost:8000/callback`
4. Click **"Save"**
5. Click **"Settings"** to view your credentials
6. Copy your **Client ID** and **Client Secret**

## Step 2: Configure Environment (1 minute)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Spotify credentials
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

On Windows:
```cmd
copy .env.example .env
notepad .env
```

## Step 3: Start the Application (2 minutes)

### Option A: Using Makefile (Recommended)
```bash
make setup
```

### Option B: Manual Setup
```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# Wait 10 seconds for services to initialize
# Then run migrations
docker-compose exec web python manage.py migrate
```

### Option C: Using Setup Scripts
**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

## Step 4: Create Admin User (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## Step 5: Test the API ✨

### Check if services are running:
```bash
curl http://localhost:8000/api/
```

### Create your first user:
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "secure123",
    "profile": {
      "favorite_genres": ["rock", "pop"],
      "moods": ["happy"]
    }
  }'
```

### Get recommendations:
```bash
# Trigger recommendation fetch (this runs asynchronously)
curl -X POST http://localhost:8000/api/recommendations/1/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"limit": 20, "seed_genres": ["rock", "pop"]}'

# Wait a few seconds, then get the recommendations
curl http://localhost:8000/api/recommendations/1/
```

## 🎉 You're All Set!

### What's Next?

- **Import Postman Collection**: Use `Music_Discovery_API.postman_collection.json` for easy testing
- **Access Admin Panel**: http://localhost:8000/admin/ (use your superuser credentials)
- **Read Full Documentation**: Check out `README.md` and `API_DOCUMENTATION.md`
- **View Logs**: `docker-compose logs -f`

### Common Commands

```bash
# Stop services
docker-compose down

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f celery

# Restart services
docker-compose restart

# Access Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web pytest
```

## Troubleshooting

### Services won't start?
```bash
# Check Docker is running
docker info

# Check logs for errors
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Can't connect to database?
```bash
# Check if PostgreSQL is healthy
docker-compose ps

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

### Spotify API errors?
- Verify your credentials in `.env`
- Check if credentials are correctly formatted (no quotes, no spaces)
- Ensure your Spotify app is not in development mode restrictions

### Port already in use?
Edit `docker-compose.yml` and change the port mappings:
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001 or another free port
```

## Need Help?

- 📖 Read the full [README.md](README.md)
- 📚 Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- 🐛 Open an issue on GitHub
- 💬 Check existing issues for solutions

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Nginx     │────▶│   Django    │────▶│ PostgreSQL  │
│  (Port 80)  │     │  (Port 8000)│     │  (Port 5432)│
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    
                           ▼                    
                    ┌─────────────┐            
                    │    Redis    │            
                    │  (Port 6379)│            
                    └─────────────┘            
                           │                    
                           ▼                    
                    ┌─────────────┐            
                    │   Celery    │            
                    │   Worker    │            
                    └─────────────┘            
```

## Sample Data Flow

1. **User creates account** → Stored in PostgreSQL
2. **User requests recommendations** → Celery task queued
3. **Celery worker** → Fetches from Spotify API
4. **Recommendations saved** → PostgreSQL + Redis cache
5. **User gets recommendations** → From Redis (fast!)
6. **User interacts** → Activity logged for analytics

---

**Happy coding! 🎵🎶**
