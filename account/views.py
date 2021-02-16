from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from news.models import Note, Comment
from django.utils import timezone


class ProfileView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request, username):
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return redirect('news')

        notes = Note.objects.filter(author=user).order_by('-post_time')

        context = {
            'user': user,
            'owner': False,
            'notes': notes
        }

        if str(user) == str(request.user):
            context['owner'] = True

        return render(request, 'account/profile.html', context)

    def post(self, request, username):
        data = request.POST

        note = Note.objects.get(pk=int(data.get('form')))
        if data.get('text') or request.FILES.get('img'):
            comment = Comment(
                author=request.user,
                text=data.get('text'),
                note=note,
                image=request.FILES.get('img'),
                post_time=timezone.now()
            )
            comment.save()

        return redirect('profile', username)
