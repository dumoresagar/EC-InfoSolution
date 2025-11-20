#!/bin/bash

# Music Discovery Backend Setup Script

echo "=========================================="
echo "Music Discovery Backend - Setup"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Spotify credentials."
    echo ""
    read -p "Press Enter to continue after updating .env file..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Building Docker containers..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "🔄 Running database migrations..."
docker-compose exec -T web python manage.py migrate

echo ""
echo "✅ Setup complete!"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo "1. Create a superuser:"
echo "   docker-compose exec web python manage.py createsuperuser"
echo ""
echo "2. Access the API:"
echo "   http://localhost:8000/api/"
echo ""
echo "3. Access Django Admin:"
echo "   http://localhost:8000/admin/"
echo ""
echo "4. View logs:"
echo "   docker-compose logs -f"
echo ""
echo "5. Stop services:"
echo "   docker-compose down"
echo "=========================================="
