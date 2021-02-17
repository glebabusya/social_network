from django.shortcuts import render
from django.views.generic import View
from . import models
from django.utils import timezone


def leave_comment(request):
    data = request.POST
    note = models.Note.objects.get(pk=int(data.get('form')))
    if data.get('text') or request.FILES.get('img'):
        comment = models.Comment(
            author=request.user,
            text=data.get('text'),
            note=note,
            image=request.FILES.get('img'),
            post_time=timezone.now()
        )
        comment.save()


class NewsView(View):
    def get(self, request):
        context = {}
        return render(request, 'news/news.html', context)

    def post(self, request):
        pass
