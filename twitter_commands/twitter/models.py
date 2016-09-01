from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Tweet(models.Model):
    class Meta:
        ordering = ['-created']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    content = models.CharField(max_length=140, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class User(AbstractUser):

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_validated = models.BooleanField(default=False)
