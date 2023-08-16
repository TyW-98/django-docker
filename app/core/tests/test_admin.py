"""
Test Django Admin interface
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Test Django admin dashboard"""

    def setUp(self):
        """Set up user and client module to use for every test""" # noqa
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpassword",
            first_name="Test First Name",
            last_name="Test Last Name"
        )

    def test_users_list(self):
        """Test new users are listed on page"""
        url = reverse('admin:core_customuser_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.email)
        self.assertContains(res, "Yes" if self.user.is_staff else "No")
        self.assertContains(res, "Yes" if self.user.is_active else "No")

    def test_admin_edit_user(self):
        """Test admin edit page for users"""
        url = reverse("admin:core_customuser_change", args=[self.user.id])
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)
        
    def test_admin_create_user(self):
        """Test admin create page for users"""
        url = reverse("admin:core_customuser_add")
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)
        