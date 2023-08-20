"""
Views for Recipe API
"""
from core.models import Recipe
from recipe import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class RecipeViewSets(viewsets.ModelViewSet):
    """View for Recipe API"""
    serializer_class = serializers.RecipeSerializer
    # Fetch all recipe data
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        authentication_classes=[TokenAuthentication]
        )
    def fetch_user_recipes(self, request):
        user_recipes = self.queryset.filter(
            user=self.request.user).order_by('id')
        serializer = self.get_serializer(user_recipes, many=True)
        return Response(serializer.data)
