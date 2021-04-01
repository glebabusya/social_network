from django.db import models
from django.conf import settings


class Community(models.Model):
    short_name = models.CharField(max_length=127, unique=True)
    title = models.CharField(max_length=127)
    current_info = models.CharField(max_length=255)

    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin')
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    avatar = models.ImageField(default='/users/user.jpg', upload_to='community')

    closed = models.BooleanField(default=False, blank=True)
