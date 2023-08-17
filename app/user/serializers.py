""" 
User's serializers
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializers for user"""
    
    class Meta: 
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        
    def create_user(self, validated_data):
        """Create and return new user with encrpyted password"""
        return get_user_model().objects.create_user(**validated_data)