from django.db import models

from django.conf import settings


class Friend(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', blank=True,
                                     on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

        friend, created = cls.objects.get_or_create(
            current_user=new_friend
        )
        friend.users.add(current_user)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

        friend, created = cls.objects.get_or_create(
            current_user=new_friend
        )
        friend.users.remove(current_user)
