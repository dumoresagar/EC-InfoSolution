.PHONY: help build up down restart logs shell migrate test clean

help:
	@echo "Music Discovery Backend - Available Commands:"
	@echo "  make build       - Build Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make shell       - Open Django shell"
	@echo "  make migrate     - Run database migrations"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean up containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started! API available at http://localhost:8000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-celery:
	docker-compose logs -f celery

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose exec web pytest

clean:
	docker-compose down -v
	@echo "Cleaned up containers and volumes"

setup: build up migrate
	@echo "Setup complete! Don't forget to create a superuser with 'make createsuperuser'"
