"""
Recipe's Serializer
"""
from core.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe"""

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_needed", "cost", "link"]
        read_only_fields = ["id"]


# Inherit functionality from RecipeSerializer
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe details"""

    # Inherit Meta used in Base RecipeSerializer
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
