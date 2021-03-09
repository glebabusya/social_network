from . import models
from django.contrib import admin


@admin.register(models.Friend)
class FriendAdmin(admin.ModelAdmin):
    pass
