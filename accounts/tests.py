from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
    
    def test_user_profile_creation(self):
        """Test if UserProfile is created automatically for a new user."""
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
    
    def test_profile_view(self):
        """Test the profile view for a logged-in user."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/accounts/profile/")
        self.assertEqual(response.status_code, 200)
