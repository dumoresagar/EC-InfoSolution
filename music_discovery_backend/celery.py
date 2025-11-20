"""
Celery configuration for music_discovery_backend project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_discovery_backend.settings')

app = Celery('music_discovery_backend')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')
