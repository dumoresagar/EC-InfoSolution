"""
URL configuration for recommendations app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'list', views.RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('user/<int:user_id>/', views.get_user_recommendations, name='user-recommendations'),
    path('user/<int:user_id>/refresh/', views.refresh_user_recommendations, name='refresh-recommendations'),
    path('', include(router.urls)),
]
