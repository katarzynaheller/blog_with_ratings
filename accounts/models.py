from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    address = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)