"""
Tests for users app.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, UserProfile


class UserModelTest(TestCase):
    """Test User model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            favorite_genres=['rock', 'pop'],
            favorite_artists=['Artist 1', 'Artist 2']
        )
    
    def test_user_creation(self):
        """Test user is created successfully."""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_profile_creation(self):
        """Test user profile is created."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(len(self.user.profile.favorite_genres), 2)


class UserAPITest(APITestCase):
    """Test User API endpoints."""
    
    def test_create_user(self):
        """Test creating a user via API."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'profile': {
                'favorite_genres': ['jazz', 'blues'],
                'moods': ['happy', 'energetic']
            }
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'newuser@example.com')
    
    def test_get_user(self):
        """Test retrieving a user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=user)
        
        response = self.client.get(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
