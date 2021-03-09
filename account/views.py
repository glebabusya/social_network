from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from news.models import Note
from django.utils import timezone
from news.views import leave_comment
from registration.models import Account
from . import forms
from .models import Friend


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
            'notes': notes,
        }

        try:
            friends = Friend.objects.get(current_user=user).users.all()
            cmn_friends = Friend.objects.get(current_user=request.user).users.exclude(pk=request.user.pk)
            common_friends = set(friends) & set(cmn_friends)
            context['friends'] = friends
            context['common_friends'] = common_friends

        except Friend.DoesNotExist:
            pass

        if str(user) == str(request.user):
            context['owner'] = True
            user.time_join = timezone.now()
            user.save()

        time_delta = timezone.now() - user.time_join

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

        if str(user) != str(request.user):
            return redirect('profile', request.user.username)

        user.time_join = timezone.now()
        user.save()

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


def change_friends(request, username, operation):
    new_friend = Account.objects.get(username=username)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
        # Отправить уведомление
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)

    return redirect('profile', new_friend.username)
