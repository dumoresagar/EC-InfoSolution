"""
Views for users app.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import User, UserProfile
from .serializers import UserSerializer, UserCreateSerializer


@method_decorator(ratelimit(key='ip', rate='10/m', method='POST'), name='create')
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations.
    
    Endpoints:
    - POST /users/ - Create a new user with profile
    - GET /users/{id}/ - Retrieve user profile
    - PUT /users/{id}/ - Update user profile
    - DELETE /users/{id}/ - Delete user
    """
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new user with profile."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return full user data
        response_serializer = UserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Update user and profile information."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def preferences(self, request, pk=None):
        """Get user preferences from profile."""
        user = self.get_object()
        try:
            profile = user.profile
            return Response({
                'favorite_genres': profile.favorite_genres,
                'favorite_artists': profile.favorite_artists,
                'moods': profile.moods,
                'preferences': profile.preferences
            })
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def update_preferences(self, request, pk=None):
        """Update user preferences."""
        user = self.get_object()
        try:
            profile = user.profile
            
            if 'favorite_genres' in request.data:
                profile.favorite_genres = request.data['favorite_genres']
            if 'favorite_artists' in request.data:
                profile.favorite_artists = request.data['favorite_artists']
            if 'moods' in request.data:
                profile.moods = request.data['moods']
            if 'preferences' in request.data:
                profile.preferences = request.data['preferences']
            
            profile.save()
            
            return Response({
                'message': 'Preferences updated successfully',
                'favorite_genres': profile.favorite_genres,
                'favorite_artists': profile.favorite_artists,
                'moods': profile.moods,
                'preferences': profile.preferences
            })
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
