"""
Serializers for users app.
"""
from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    class Meta:
        model = UserProfile
        fields = [
            'favorite_genres',
            'favorite_artists',
            'moods',
            'preferences',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Create user with profile."""
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        
        # Create profile
        UserProfile.objects.create(user=user, **profile_data)
        
        return user
    
    def update(self, instance, validated_data):
        """Update user and profile."""
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        
        # Update profile if data provided
        if profile_data is not None:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'profile'
        ]
    
    def create(self, validated_data):
        """Create user with hashed password and profile."""
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile
        UserProfile.objects.create(user=user, **profile_data)
        
        return user
