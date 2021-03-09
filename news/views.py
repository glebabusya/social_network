from django.shortcuts import render, redirect
from django.views.generic import View

from registration.models import Account
from . import models
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Note, Like


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
    # Отправить уведомление


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
        try:
            note = models.Note(author=request.user, post_time=timezone.now(), text=request.POST.get('note_text'),
                               image1=files[0], image2=files[1], image3=files[2])
        except IndexError:
            try:
                note = models.Note(author=request.user, post_time=timezone.now(), text=request.POST.get('note_text'),
                                   image1=files[0], image2=files[1])
            except IndexError:
                try:
                    note = models.Note(author=request.user, post_time=timezone.now(),
                                       text=request.POST.get('note_text'),
                                       image1=files[0])
                except IndexError:
                    if request.POST.get('note_text'):
                        note = models.Note(author=request.user, post_time=timezone.now(),
                                           text=request.POST.get('note_text'),
                                           )
                    else:
                        return redirect('profile', request.user.username)

        note.save()

        return redirect('news')


def like(request, note_pk, back_url, username=None):
    user = request.user
    note = Note.objects.get(pk=note_pk)
    try:
        liked = Like.objects.get(user=user, note=note)
        liked.delete()
    except Like.DoesNotExist:
        Like(user=user, note=note).save()
    if username:
        return redirect(back_url, username)
    else:
        return redirect(back_url)
    # Отправить уведомление
