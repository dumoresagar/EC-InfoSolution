@echo off
REM Music Discovery Backend Setup Script for Windows

echo ==========================================
echo Music Discovery Backend - Setup
echo ==========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Warning: No .env file found. Copying from .env.example...
    copy .env.example .env
    echo .env file created. Please edit it with your Spotify credentials.
    echo.
    pause
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

echo Building Docker containers...
docker-compose build

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo Running database migrations...
docker-compose exec -T web python manage.py migrate

echo.
echo Setup complete!
echo.
echo ==========================================
echo Next Steps:
echo ==========================================
echo 1. Create a superuser:
echo    docker-compose exec web python manage.py createsuperuser
echo.
echo 2. Access the API:
echo    http://localhost:8000/api/
echo.
echo 3. Access Django Admin:
echo    http://localhost:8000/admin/
echo.
echo 4. View logs:
echo    docker-compose logs -f
echo.
echo 5. Stop services:
echo    docker-compose down
echo ==========================================
pause
