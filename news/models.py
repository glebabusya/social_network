from django.conf import settings
from django.db import models
from django.utils import timezone

from community.models import Community
from registration.models import Account


class Note(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    group = models.ForeignKey(to=Community, on_delete=models.PROTECT, blank=True, null=True)
    post_time = models.DateTimeField(default=timezone.now)
    text = models.TextField(blank=True)
    image1 = models.ImageField(blank=True, upload_to='notes')
    image2 = models.ImageField(blank=True, upload_to='notes')
    image3 = models.ImageField(blank=True, upload_to='notes')
    can_comment = models.BooleanField(default=True)

    def liked(self):
        liked = self.like_set.values_list('user', flat=True)
        return liked

    def liked_6(self):
        user_likes = self.liked()[:6]
        users = []
        for user_pk in user_likes:
            users.append(Account.objects.get(pk=user_pk))
        return users


class Comment(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    text = models.CharField(max_length=2000, blank=True)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE, blank=True, related_query_name='comment')
    image = models.ImageField(blank=True, upload_to='comments', )
    post_time = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE, blank=True)
