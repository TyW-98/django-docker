"""
Test Custom user model
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):
    """Test Case"""

    def test_create_user_with_email(self):
        """Test creating user with email"""
        email = "test@example.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalised_emaiL(self):
        """Test normalisation of new user's email"""
        sample_emails = [
            ["email1@EXAMPLE.com", "email1@example.com"],
            ["Email2@Example.com", "Email2@example.com"],
            ["EMAIL3@EXAmple.com", "EMAIL3@example.com"],
            ["email4@example.COM", "email4@example.com"]
        ]

        for test_email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(test_email,"samplepassword")

            self.assertEqual(user.email, expected_email)
            
    def test_new_user_empty_email_error(self):
        """Raise Error if no email is passed in"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpassword")
            
    def test_create_super_user(self):
        """Test creating super user"""
        email = "test@example.com"
        password = "testpassword"
        super_user = get_user_model().objects.create_superuser(
            email = email, 
            password = password
            )
        
        self.assertEqual(super_user.email, email)
        self.assertTrue(super_user.check_password(password))
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
            