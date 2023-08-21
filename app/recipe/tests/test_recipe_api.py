"""
Tests for Recipe API
"""

from datetime import timedelta
from decimal import Decimal

from core.models import Recipe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse("recipe:recipe-list")
USER_SPECIFIC_RECIPE_URL = reverse("recipe:recipe-fetch-user-recipes")


def recipe_detail_url(recipe_id):
    """Create dynamic recipe detail URL"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a recipe for testing"""
    default_recipe = {
        "title": "Sample Recipe",
        "time_needed": 60,
        "cost": Decimal(5.99),
        "description": "Test Recipe Description",
        "link": "http:example.com/test_recipe.pdf/"
    }
    # Overwrite default recipe dictionary with any values passed into params
    default_recipe.update(params)
    return Recipe.objects.create(user=user, **default_recipe)


class PublicRecipeAPITest(TestCase):
    """Test unauthenticated Recipe API request"""

    def setUp(self):
        self.client = APIClient()

    def test_list_recipe(self):
        """Test successfully fetch API without authentication"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthenticate_create_recipe(self):
        """Test creating recipes without authentication"""
        test_recipe_payload = {
            "title": "test recipe title",
            "time_needed": 43,
            "cost": Decimal("5.32"),
            "description": "test recipe description",
            "link": "http://example.com"
        }
        res = self.client.post(RECIPE_URL, test_recipe_payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            res.data,
            {
                'detail': "You would need to register an account to create recipes" # noqa
            }
        )
        # Ensure no recipes was created
        self.assertEqual(Recipe.objects.count(), 0)


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
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        # Retrieving all recipes
        recipes = Recipe.objects.all().order_by("id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieving_user_recipes(self):
        """Test retrieving specific user's recipes"""
        second_test_user_details = {
            "email": "test2@example.com",
            "password": "password",
            "first_name": "first 2",
            "last_name": "last 2"
        }
        test_user2 = get_user_model().objects.create_user(
            **second_test_user_details
        )
        create_recipe(user=self.user)
        create_recipe(user=test_user2)

        res = self.client.get(USER_SPECIFIC_RECIPE_URL)
        # Retrieving user specific recipes
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieving_recipe_details(self):
        """Test retrieving specific recipe's details"""
        test_recipe = create_recipe(user=self.user)

        res = self.client.get(recipe_detail_url(test_recipe.id))
        serializer = RecipeDetailSerializer(test_recipe, many=False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating new recipes"""
        # Dont need pass in user as argument as it is already logged in in setUp # noqa
        test_recipe_payload = {
            "title": "test recipe title",
            "time_needed": 43,
            "cost": Decimal("5.32"),
            "description": "test recipe description",
            "link": "http://example.com"
        }
        # Make HTTP post request to URL
        res = self.client.post(RECIPE_URL, test_recipe_payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve specific recipe using id returned from res
        created_recipe = Recipe.objects.get(id=res.data["id"])

        # Check the values of every items in created_recipe obj
        for key, value in test_recipe_payload.items():
            self.assertEqual(getattr(created_recipe, key), value)

        # Check if the user in the recipe matches the one used to create
        self.assertEqual(created_recipe.user, self.user)

    def test_update_recipe(self):
        """Test only allow recipe owner to update recipe details"""
        test_recipe_payload = {
            "title": "test recipe title",
            "time_needed": 43,
            "cost": Decimal("5.32"),
            "description": "test recipe description",
            "link": "http://example.com"
        }
        res = self.client.post(RECIPE_URL, test_recipe_payload)
        # Check status of creating new recipe
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Recipe's new details
        new_recipe_payload = {
            "title": "update title",
        }
        # Fetch the recipe that needs to be updated
        update_recipe = Recipe.objects.get(id=res.data["id"])
        # Send HTTP patch request to update recipe details
        res = self.client.patch(
            recipe_detail_url(res.data["id"]),
            new_recipe_payload
        )
        # Check status of patch request
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Refresh database
        update_recipe.refresh_from_db()
        # Check values in updated recipe
        for key, value in new_recipe_payload.items():
            self.assertEqual(getattr(update_recipe, key), value)
        # Check last modified time is updated
        time_difference = timezone.now() - update_recipe.last_modified
        # Set time threshold
        maximum_time_difference = timedelta(seconds=1)
        # Check last_modified time in recipe is updated
        self.assertLessEqual(time_difference, maximum_time_difference)
