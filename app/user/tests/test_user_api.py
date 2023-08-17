"""
Test User API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import APIClient, status

# Get URL from name of view (app:endpoint)
CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    """Create and return a new user for testing"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test Publicly accessible features"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user is successful"""
        payload = {
            "email": "user@example.com",
            "password": "testpassword",
            "first_name": "test First Name",
            "last_name": "test Last name"
        }
        # Make HTTP post request to CREATE_USER_URL
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve user from database by searching for email (Check if user is created in database) # noqa
        user = get_user_model().objects.get(email=payload["email"])
        # Check if user password matches payload password
        self.assertTrue(user.check_password(payload["password"]))
        # Check password hash is not in responds data
        self.assertNotIn("password", res.data)

    def test_user_email_unique(self):
        """Test user email to be unique"""
        payload = {
            "email": "user@example.com",
            "password": "testpassword",
            "first_name": "test First Name",
            "last_name": "test Last name"
        }
        # (**payload) <- Will spread dictionary items into individual arguments # noqa
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test length of password. Less than 5"""
        payload = {
            "email": "user@example.com",
            "password": "pwd",
            "first_name": "test First Name",
            "last_name": "test Last name"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if user is created as it shouldn't
        user_exist = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exist)
