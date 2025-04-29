"""Test views in the core app."""

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse


class LogoutViewTests(TestCase):
    """Test the logout view."""

    def setUp(self):
        """Create a test user and client."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.logout_url = reverse("core:logout")

    def test_logout_view_get_authenticated(self):
        """Test GET request to logout view when user is authenticated."""
        # Log in the user
        self.client.login(username="testuser", password="testpass123")
        
        # Make GET request to logout page
        response = self.client.get(self.logout_url)
        
        # Check that we get 200 OK and the correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/logout.html")

    def test_logout_view_get_unauthenticated(self):
        """Test GET request to logout view when user is not authenticated."""
        # Make GET request to logout page without logging in
        response = self.client.get(self.logout_url)
        
        # Check that we get redirected to home
        self.assertRedirects(response, reverse("core:home"))

    def test_logout_view_post_authenticated(self):
        """Test POST request to logout view when user is authenticated."""
        # Log in the user
        self.client.login(username="testuser", password="testpass123")
        
        # Make POST request to logout
        response = self.client.post(self.logout_url)
        
        # Check that we get redirected to home
        self.assertRedirects(response, reverse("core:home"))
        
        # Check that the user is logged out
        self.assertFalse("_auth_user_id" in self.client.session)
        
        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have been logged out successfully.")

    def test_logout_view_post_unauthenticated(self):
        """Test POST request to logout view when user is not authenticated."""
        # Make POST request to logout without logging in
        response = self.client.post(self.logout_url)
        
        # Check that we get redirected to home
        self.assertRedirects(response, reverse("core:home")) 