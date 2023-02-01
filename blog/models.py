from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime


class Category(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"pk": self.pk})


class Post(models.Model):
    title = models.CharField(max_length=140)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    body = models.TextField()
    category = models.ManyToManyField(Category)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    # like = models.ManyToManyField("auth.User", related_name="blog_posts")

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
