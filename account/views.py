from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from news.models import Note, Comment
from django.utils import timezone
from news.views import leave_comment
from . import forms
import datetime


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
            user.time_join = timezone.now()
            user.save()

        # Determining how long a user has been online
        now = str(timezone.now())
        user_join = str(user.time_join)

        y1 = int(now[:4])
        m1 = int(now[5:7])
        d1 = int(now[8:10])
        h1 = int(now[11:13])
        min1 = int(now[14:16])

        y2 = int(user_join[:4])
        m2 = int(user_join[5:7])
        d2 = int(user_join[8:10])
        h2 = int(user_join[11:13])
        min2 = int(user_join[14:16])

        d1 = datetime.datetime(y1, m1, d1, h1, min1)
        d2 = datetime.datetime(y2, m2, d2, h2, min2)
        time_delta = d1 - d2

        if time_delta.total_seconds() < 300:
            context['time_delta'] = 'Online'
        elif time_delta.total_seconds() < 3600:
            context['time_delta'] = f'Was online {str(time_delta)[2:4]} minutes ago'
        else:
            context['time_delta'] = f'Was online {user.time_join.strftime(" %d %B")}'

        return render(request, 'account/profile.html', context)

    def post(self, request, username):
        leave_comment(request)
        return redirect('profile', username)


class RedactProfileView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, request, username):
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return redirect('news')

        form = forms.ProfileForm(instance=user)

        context = {
            'user': user,
            'form': form
        }

        return render(request, 'account/redact.html', context)

    def post(self, request, username):
        user = request.user
        form = forms.ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('profile', username)
