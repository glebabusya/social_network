from django.contrib import admin
from . import models


@admin.register(models.Community)
class CommunityAdmin(admin.ModelAdmin):
    pass
