from django.db import connection
from django.shortcuts import render, redirect
from django.views.generic import View

from groups.models import Group
from registration.models import Account
from . import models
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Note, Like


def change_comment(request, note_pk, back_url, *args, **kwargs):
    try:
        note = Note.objects.get(pk=note_pk)
        if note.can_comment:
            note.can_comment = False
        else:
            note.can_comment = True

        note.save()
    except Note.DoesNotExist:
        pass

    return redirect(back_url, *args, **kwargs)


def like(request, note_pk, back_url, *args, **kwargs):  # Переделать Лайк#
    user = request.user
    note = Note.objects.get(pk=note_pk)
    try:
        liked = Like.objects.get(user=user, note=note)
        liked.delete()
    except Like.DoesNotExist:
        Like(user=user, note=note).save()
    if args or kwargs:
        return redirect(back_url, *args, **kwargs)
    else:
        return redirect(back_url)
    # Отправить уведомление


def delete_note(request, note_pk, back_url, *args, **kwargs):
    try:
        note = Note.objects.get(author=request.user, pk=note_pk)
        note.delete()
    except Note.DoesNotExist:
        pass
    return redirect(back_url, *args, **kwargs)


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


class NewsView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request):
        context = {}
        return render(request, 'news/news.html', context)

    def post(self, request):
        pass


class AddNoteView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request, group_name=None):
        context = {}
        if group_name:
            try:
                group = Group.objects.get(admin=request.user, short_name=group_name)
                context['author'] = group
                context['back_url'] = 'group'
                context['back_url_data'] = group.short_name
            except Group.DoesNotExist:
                return redirect('news')
        else:
            context['author'] = request.user
            context['back_url'] = 'profile'
            context['back_url_data'] = request.user.username
        return render(request, 'news/add_note.html', context)

    def post(self, request, group_name=None):
        files = request.FILES.getlist('note_img')
        if group_name:
            try:
                group = Group.objects.get(admin=request.user, short_name=group_name)
                try:
                    note = models.Note(group=group, post_time=timezone.now(),
                                       text=request.POST.get('note_text'),
                                       image1=files[0], image2=files[1], image3=files[2])
                except IndexError:
                    try:
                        note = models.Note(group=group, post_time=timezone.now(),
                                           text=request.POST.get('note_text'),
                                           image1=files[0], image2=files[1])
                    except IndexError:
                        try:
                            note = models.Note(group=group, post_time=timezone.now(),
                                               text=request.POST.get('note_text'),
                                               image1=files[0])
                        except IndexError:
                            if request.POST.get('note_text'):
                                note = models.Note(group=group, post_time=timezone.now(),
                                                   text=request.POST.get('note_text'),
                                                   )
                            else:
                                return redirect('group', group.short_name)

            except Group.DoesNotExist:
                return redirect('news')
        else:
            try:
                note = models.Note(author=request.user, post_time=timezone.now(), text=request.POST.get('note_text'),
                                   image1=files[0], image2=files[1], image3=files[2])
            except IndexError:
                try:
                    note = models.Note(author=request.user, post_time=timezone.now(),
                                       text=request.POST.get('note_text'),
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
        if group_name:
            return redirect('group', group.short_name)
        else:
            return redirect('profile', request.user.username)


class NoteView(LoginRequiredMixin, View):
    login_url = 'registration'

    # такие аргументы нужны для того чтобы не создавать отдельную функцию для лайка...
    def get(self, request, note_id, url, name=None):
        try:
            note = models.Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            if name:
                return redirect(url, name)
            else:
                return redirect(url)
        user = note.author
        context = {
            'url': 'note',
            'note': note,
            'user': user,
            'back_url': url,
            'username': name
        }
        return render(request, 'news/note.html', context)

    def post(self, request, *args, **kwargs):
        leave_comment(request)
        return redirect('note', *args, **kwargs)
