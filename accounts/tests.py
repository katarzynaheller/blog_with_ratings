from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser


class SignupPageTests(TestCase):
    def test_url_exist_at_correct_location(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, "testuser")


class LoginPageTests(TestCase):
    def setUp(self):
        # can’t set the user’s password by setting the password attribute directly
        # (you need to use the set_password() function).
        # Alternatively, use the create_user() helper method to create a new user with a correctly hashed password.
        self.user = CustomUser.objects.create(username="testuser", password="secret")
        self.user.set_password("secret")
        self.user.save()
        self.client = Client()
        self.assertTrue(self.client.login(username="testuser", password="secret"))

    def test_login_page(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, self.user.username)

    def test_logout_page(self):
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, self.user.username)
