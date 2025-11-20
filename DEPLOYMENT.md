# Deployment Guide

This guide covers deploying the Music Discovery Backend to production environments.

## Table of Contents
- [Production Checklist](#production-checklist)
- [Environment Configuration](#environment-configuration)
- [Deployment Options](#deployment-options)
- [Security Hardening](#security-hardening)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)
- [Scaling](#scaling)

---

## Production Checklist

### Before Deployment

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up SSL/TLS certificates
- [ ] Configure production database credentials
- [ ] Set strong passwords for all services
- [ ] Review and update CORS settings
- [ ] Enable proper logging
- [ ] Set up monitoring and alerts
- [ ] Configure backup strategy
- [ ] Test all endpoints
- [ ] Run security audit
- [ ] Document environment variables
- [ ] Set up CI/CD pipeline (optional)

### Security Checklist

- [ ] All secrets in environment variables
- [ ] HTTPS/SSL enabled
- [ ] Database connections encrypted
- [ ] Rate limiting configured
- [ ] CORS properly restricted
- [ ] Admin panel secured
- [ ] File upload restrictions
- [ ] Regular security updates

---

## Environment Configuration

### Production .env File

```bash
# Django Settings
SECRET_KEY=<GENERATE_RANDOM_50_CHAR_KEY>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
POSTGRES_DB=music_discovery_prod
POSTGRES_USER=produser
POSTGRES_PASSWORD=<STRONG_PASSWORD>
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=<STRONG_PASSWORD>  # Add password

# Spotify API Configuration
SPOTIFY_CLIENT_ID=<YOUR_CLIENT_ID>
SPOTIFY_CLIENT_SECRET=<YOUR_CLIENT_SECRET>
SPOTIFY_REDIRECT_URI=https://yourdomain.com/callback

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<APP_PASSWORD>
EMAIL_USE_TLS=True

# Sentry (Error Tracking - Optional)
SENTRY_DSN=<YOUR_SENTRY_DSN>
```

### Generate Secret Key

```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## Deployment Options

### Option 1: Docker on VPS (DigitalOcean, Linode, AWS EC2)

#### 1. Provision Server
```bash
# Minimum requirements:
# - 2 CPU cores
# - 4GB RAM
# - 40GB SSD
# - Ubuntu 22.04 LTS
```

#### 2. Install Docker
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. Clone & Configure
```bash
# Clone repository
git clone <your-repo-url>
cd music_discovery_backend

# Create .env file
nano .env
# Add production configuration

# Create SSL certificates directory
mkdir -p certbot/conf certbot/www
```

#### 4. Set Up SSL with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

#### 5. Update nginx.conf for SSL
```nginx
events {
    worker_connections 1024;
}

http {
    upstream web {
        server web:8000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /app/staticfiles/;
        }

        client_max_body_size 10M;
    }
}
```

#### 6. Update docker-compose.yml for SSL
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - web
```

#### 7. Deploy
```bash
# Build and start
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

#### 8. Set Up Auto-Restart
```bash
# Create systemd service
sudo nano /etc/systemd/system/music-discovery.service
```

```ini
[Unit]
Description=Music Discovery Backend
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/music_discovery_backend
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl enable music-discovery
sudo systemctl start music-discovery
```

---

### Option 2: AWS Elastic Beanstalk

#### 1. Install EB CLI
```bash
pip install awsebcli
```

#### 2. Initialize EB
```bash
eb init -p docker music-discovery-backend
```

#### 3. Create Environment
```bash
eb create production-env
```

#### 4. Deploy
```bash
eb deploy
```

---

### Option 3: Kubernetes (Advanced)

#### 1. Create Kubernetes Manifests
Create `k8s/` directory with:
- `deployment.yaml`
- `service.yaml`
- `ingress.yaml`
- `configmap.yaml`
- `secrets.yaml`

#### 2. Deploy
```bash
kubectl apply -f k8s/
```

---

## Security Hardening

### 1. Update settings.py for Production

```python
# Add to settings.py

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS - Restrict to your domain
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

### 2. Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 3. Regular Updates
```bash
# Create update script
cat > update.sh << 'EOF'
#!/bin/bash
cd /path/to/music_discovery_backend
git pull
docker-compose down
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
EOF

chmod +x update.sh
```

---

## Monitoring & Logging

### 1. Set Up Log Aggregation
```bash
# View logs
docker-compose logs -f

# Save logs to file
docker-compose logs > logs.txt
```

### 2. Install Monitoring Tools

#### Option A: Prometheus + Grafana
```yaml
# Add to docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

#### Option B: Cloud Monitoring
- AWS CloudWatch
- Google Cloud Monitoring
- Datadog
- New Relic

### 3. Error Tracking with Sentry

```python
# Install sentry-sdk
pip install sentry-sdk

# Add to settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True
    )
```

---

## Backup & Recovery

### 1. Database Backup Script
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

docker-compose exec -T db pg_dump -U postgres music_discovery_db > \
  $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
EOF

chmod +x backup.sh

# Schedule with cron
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### 2. Restore from Backup
```bash
# Stop application
docker-compose down

# Restore database
docker-compose up -d db
docker-compose exec -T db psql -U postgres music_discovery_db < backup.sql

# Start application
docker-compose up -d
```

---

## Scaling

### Horizontal Scaling

#### 1. Load Balancer Setup
```nginx
upstream backend {
    server web1:8000;
    server web2:8000;
    server web3:8000;
}
```

#### 2. Multiple Workers
```yaml
# docker-compose.yml
services:
  web:
    deploy:
      replicas: 3
```

### Vertical Scaling

```yaml
# Increase resources
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Database Scaling

- Read replicas for PostgreSQL
- Redis cluster for caching
- Connection pooling with PgBouncer

---

## Performance Optimization

### 1. Enable Query Caching
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
        }
    }
}
```

### 2. Database Connection Pooling
```python
# settings.py
DATABASES['default']['CONN_MAX_AGE'] = 600
```

### 3. Increase Celery Workers
```yaml
# docker-compose.yml
celery:
  command: celery -A music_discovery_backend worker --concurrency=8 --loglevel=info
```

---

## Troubleshooting Production Issues

### High Memory Usage
```bash
# Check memory
docker stats

# Restart services
docker-compose restart
```

### Slow Queries
```bash
# Enable query logging
docker-compose exec db psql -U postgres -c "ALTER SYSTEM SET log_statement = 'all';"
docker-compose restart db

# View logs
docker-compose logs db | grep "SELECT"
```

### Celery Tasks Stuck
```bash
# Purge queue
docker-compose exec celery celery -A music_discovery_backend purge

# Restart workers
docker-compose restart celery
```

---

## Maintenance Windows

Schedule regular maintenance:
1. Weekly database backups
2. Monthly security updates
3. Quarterly dependency updates
4. Log rotation and cleanup

---

## Support & Resources

- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Docker Production: https://docs.docker.com/engine/swarm/
- PostgreSQL Backup: https://www.postgresql.org/docs/current/backup.html

---

**Remember**: Always test in staging before deploying to production!
