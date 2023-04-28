from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from blog.views import get_top_rated_posts

from .models import Post, Rating
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
        self.assertContains(response, "posts")

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

class PostRatingTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser1", password="secret1")
        self.user.set_password("secret1")
        self.user.save()
        self.client = Client()
        self.assertTrue(self.client.login(username="testuser1", password="secret1"))

        # create a post with a rating
        self.post_with_rating = Post.objects.create(
            title='Test post with rating',
            body='This is a test post with a rating',
            author=self.user,
        )
        Rating.objects.create(
            post=self.post_with_rating,
            user=self.user,
            rating=4
        )

        # create a post without a rating
        self.post_without_rating = Post.objects.create(
            title='Test post without rating',
            body='This is a test post without a rating',
            author=self.user,
        )
    # check if function return correct value
    def test_get_top_rated_posts(self):
        top_posts = get_top_rated_posts()
        self.assertEqual(top_posts.count(), 1)
        self.assertEqual(top_posts[0].id, self.post_with_rating.id)

class NoRatedPostsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser1", password="secret1")
        self.user.set_password("secret1")
        self.user.save()
        self.client = Client()
        self.assertTrue(self.client.login(username="testuser1", password="secret1"))

        # create two posts without a rating
        self.post_without_rating = Post.objects.create(
            title='Test post without rating',
            body='This is a test post without a rating',
            author=self.user,
        )

        self.post_without_rating = Post.objects.create(
            title='Test second post without rating',
            body='This is a second test post without a rating',
            author=self.user,
        )

    # check function when no rated posts
    def test_no_rated_posts(self):
        top_posts = get_top_rated_posts()
        self.assertEqual(top_posts.count(), 0)

    # home "top rated posts" section hidden when empty
    def test_empty_top_rated(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Top rated posts")

class SameRatingTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser1", password="secret1")
        self.user.set_password("secret1")
        self.user.save()
        self.client = Client()
        self.assertTrue(self.client.login(username="testuser1", password="secret1"))

    # create posts with different ratings
        self.post1 = Post.objects.create(
            title='Test post 1',
            body='This is test post 1',
            author=self.user,
        )
        Rating.objects.create(
            post=self.post1,
            user=self.user,
            rating=4
        )

        self.post2 = Post.objects.create(
            title='Test post 2',
            body='This is test post 2',
            author=self.user,
        )
        Rating.objects.create(
            post=self.post2,
            user=self.user,
            rating=5
        )

        # create posts with the same rating
        self.post3 = Post.objects.create(
            title='Test post 3',
            body='This is test post 3',
            author=self.user,
        )
        Rating.objects.create(
            post=self.post3,
            user=self.user,
            rating=3
        )

        self.post4 = Post.objects.create(
            title='Test post 4',
            body='This is test post 4',
            author=self.user,
        )
        Rating.objects.create(
            post=self.post4,
            user=self.user,
            rating=3
        )

    def test_the_same_rating_posts(self):
        top_posts = get_top_rated_posts()
        
        # assert that the top_posts queryset contains two posts
        self.assertEqual(top_posts.count(), 4)
        
        # assert that the post with the highest rating is on top
        self.assertEqual(top_posts[0].title, self.post2.title)
        self.assertEqual(top_posts[1].title, self.post1.title)

        #assert that posts with the same ratings are included in list
        self.assertNotEqual(top_posts[1].title, self.post3.title)
        self.assertIn(self.post3, top_posts)
        self.assertNotEqual(top_posts[1].title, self.post4.title)
        self.assertIn(self.post4, top_posts)
        
        
       