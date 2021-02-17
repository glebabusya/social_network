from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from news.models import Note, Comment
from django.utils import timezone
from news.views import leave_comment
from . import forms


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
