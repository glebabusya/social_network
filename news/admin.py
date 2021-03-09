from . import models
from django.contrib import admin


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    pass
