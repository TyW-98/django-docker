"""
Views for USER API
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """HTTP post request to create new user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create login token for users"""
    serializer_class = AuthTokenSerializer
    # For django rest_framework browseable-api view
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
