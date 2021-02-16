from django.conf import settings
from django.db import models
from django.utils import timezone


class Note(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    # group = models.OneToOneField()
    post_time = models.DateTimeField()
    liked = models.PositiveIntegerField(blank=True, default=0)
    text = models.TextField(blank=True)
    image1 = models.ImageField(blank=True, upload_to='notes')
    image2 = models.ImageField(blank=True, upload_to='notes')
    image3 = models.ImageField(blank=True, upload_to='notes')
    can_comment = models.BooleanField(default=True)


class Comment(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    text = models.CharField(max_length=2000, blank=True)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE, blank=True, related_query_name='comment')
    image = models.ImageField(blank=True, upload_to='comments', )
    post_time = models.DateTimeField()
