"""
URL configuration for analytics app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activity', views.UserActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.analytics_summary, name='analytics-summary'),
    path('trends/', views.analytics_trends, name='analytics-trends'),
    path('user/<int:user_id>/', views.user_engagement, name='user-engagement'),
]
