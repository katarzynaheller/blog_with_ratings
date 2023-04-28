from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=140)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    category = models.ManyToManyField(Category)
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-pub_date"]

    def average_rating(self):
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=""
    )
    rating = models.FloatField()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
