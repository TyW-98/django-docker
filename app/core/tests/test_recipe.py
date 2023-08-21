"""
Tests for recipe model
"""
from decimal import Decimal

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


class RecipeTests(TestCase):

    def test_create_recipe(self):
        """Test creating recipe is successfull"""
        sample_user = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        user = get_user_model().objects.create_user(**sample_user)

        sample_recipe = {
            "title": "Sample Recipe",
            "time_needed": 5,
            "cost": Decimal("9.99"),
            "description": "Sample recipe description"
        }
        recipe = models.Recipe.objects.create(
            user=user,
            **sample_recipe
        )

        self.assertEqual(str(recipe), sample_recipe["title"])
