from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from .models import Post
from accounts.models import CustomUser


class PostDetailTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", password="secret")
        self.user.set_password("secret")
        self.user.save()
        self.client = Client()
        self.assertTrue(self.client.login(username="testuser", password="secret"))

        self.post = Post.objects.create(
            title="Test post",
            body="Nice body content",
            author=self.user,
        )

    def test_user(self):
        self.assertTrue(isinstance(self.user, CustomUser))

    def test_post_model(self):
        self.assertEqual(self.post.title, "Test post")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/10000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Rate")

    def test_rating_post(self):
        response = self.client.post(
            reverse("post_rate", kwargs={"pk": self.post.pk}),
            {
                "rate": "5",
                "user": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
