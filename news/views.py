from django.shortcuts import render, redirect
from django.views.generic import View
from . import models
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


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


class AddNoteView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'news/add_note.html', context)

    def post(self, request):
        files = request.FILES.getlist('note_img')

        note = models.Note(author=request.user, post_time=timezone.now(), text=request.POST.get('note_text'),
                           image1=files[0], image2=files[1], image3=files[2])
        note.save()

        return redirect('news')
