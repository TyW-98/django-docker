""" 
Tests for Recipe API
"""

from decimal import Decimal

from core.models import Recipe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse("recipe:recipe-list")
USER_RECIPE_URL = reverse("recipe:user-recipe")

def create_recipe(user, **params): 
    """Create and return a recipe for testing"""
    default_recipe = {
        "title":"Sample Recipe",
        "time_needed":60,
        "cost": Decimal(5.99),
        "description": "Test Recipe Description",
        "link": "http:example.com/test_recipe.pdf/"
    }
    # Overwrite default recipe dictionary with any values passed into params
    default_recipe.update(params)
    return Recipe.objects.create(user, **default_recipe)

class PublicRecipeAPITest(TestCase):
    """Test unauthenticated Recipe API request"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_list_recipe(self):
        """Test successfully fetch API without authentication"""
        res = self.client.get(RECIPE_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

class PrivateRecipeAPITest(TestCase):
    """Test recipe API requests that requires authentication"""
    
    def setUp(self):
        """Setup user and APIClient which will be used in each test"""
        test_user_details = {
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "first",
            "last_name": "last_name"
        }
        self.user = get_user_model().objects.create_user(**test_user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_recipes(self):
        """Test retrieving recipes"""
        create_recipe(self.user)
        create_recipe(self.user)
        
        res = self.client.get(RECIPE_URL)
        # Retrieving all recipes
        recipes = Recipe.objects.all().order_by("id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer)
        
    def test_retrieving_user_recipes(self):
        """Test retrieving user's recipes"""
        second_test_user_details = {
            "email": "test2@example.com",
            "password": "password",
            "first_name": "first 2",
            "last_name": "last 2"
        }
        test_user2 = get_user_model().objects.create_user(**second_test_user_details)
        create_recipe(self.user)
        create_recipe(test_user2)
        
        res = self.client.get(USER_RECIPE_URL)
        # Retrieving user specific recipes
        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer)
        