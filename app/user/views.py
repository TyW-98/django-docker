""" 
Views for USER API
"""
from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """HTTP post request to create new user"""
    serializer_class = UserSerializer