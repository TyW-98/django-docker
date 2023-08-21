"""
Views for Recipe API
"""
from core.models import Recipe
from django.utils import timezone
from recipe import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class RecipeViewSets(viewsets.ModelViewSet):
    """View for Recipe API"""
    serializer_class = serializers.RecipeDetailSerializer
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
        serializer = serializers.RecipeSerializer(user_recipes, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """When new object is created this method will execute"""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied(
                "You would need to register an account to create recipes"
            )

    def perform_update(self, serializer):
        """Execute when updating recipe"""
        recipe_details = serializer.instance

        if self.request.user.is_authenticated and recipe_details.user == self.request.user: # noqa
            recipe_details.last_modified = timezone.now()
            recipe_details.save()
            serializer.save()
        else:
            raise PermissionDenied(
                "You do not have permission to edit the recipe"
            )
