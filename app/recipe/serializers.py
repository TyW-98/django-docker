"""
Recipe's Serializer
"""
from core.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe"""

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_needed", "cost", "description", "link"]
        read_only_fields = ["id"]
