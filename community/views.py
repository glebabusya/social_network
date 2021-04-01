from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from account.models import Friend
from news.models import Note
from . import models, forms
# Create your views here.
from django.views.generic.base import View


def subscribe(request, name):
    try:
        group = models.Community.objects.get(short_name=name)
        group.subscribers.add(request.user)
    except models.Community.DoesNotExist:
        pass
    return redirect('group', name)


def unsubscribe(request, name):
    try:
        group = models.Community.objects.get(short_name=name)
        group.subscribers.remove(request.user)
    except models.Community.DoesNotExist:
        pass
    return redirect('group', name)


class GroupView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request, name):
        try:
            group = models.Community.objects.get(short_name=name)
        except models.Community.DoesNotExist:
            return redirect('news')

        context = {
            'group': group,
            'admin': False,
            'back_url': 'group',
            'name': group.short_name
        }

        if group.admin == request.user:
            context['admin'] = True

        subscribers = group.subscribers.all()
        context['subscribers'] = subscribers

        friends = Friend.objects.get(current_user=request.user).users.all()
        subscribed_friends = set(friends) & set(set(subscribers))
        context['subscribed_friends'] = subscribed_friends

        notes = Note.objects.filter(group=group).order_by('-post_time')

        context['notes'] = notes
        return render(request, 'community/group.html', context)

    def post(self, request, name):
        pass


class RedactGroupView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request, name):
        try:
            group = models.Community.objects.get(short_name=name)
        except models.Community.DoesNotExist:
            return redirect('group', name)
        form = forms.GroupForm(instance=group)

        context = {
            'form': form
        }
        return render(request, 'community/redact_group.html', context)

    def post(self, request, name):
        try:
            group = models.Community.objects.get(short_name=name)
        except models.Community.DoesNotExist:
            return redirect('group', name)
        form = forms.GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()

        return redirect('group', name)


class GroupsView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request, search=None):
        context = {
            'search': search
        }
        users = tuple(models.Community.objects.all().values_list('subscribers', flat=True))
        if search:
            my_groups = models.Community.objects.raw(
                f"SELECT * FROM community_community WHERE {request.user.id} in {users} and short_name LIKE '%%{search}%%' or title LIKE '%%{search}%%'")
            all_groups = models.Community.objects.raw(
                f"SELECT * FROM community_community WHERE short_name LIKE '%%{search}%%' or title LIKE '%%{search}%%'")
            print(my_groups)
            context['my_groups'] = my_groups
            context['all_groups'] = all_groups
            for group in my_groups:
                print(group.title)
        else:
            context['my_groups'] = request.user.community_set.all()

        return render(request, 'community/groups.html', context)

    def post(self, request, search=None):
        s = request.POST.get('search')
        if s:
            return redirect('groups', s)
        else:
            return redirect('groups')


class CreateGroupView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request):
        form = forms.GroupForm()
        context = {
            'form': form
        }
        return render(request, 'community/create_group.html', context)

    def post(self, request):
        form = forms.GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['short_name']
            print(name)

            return redirect('group', name)

        return render(request, 'community/create_group.html', {'form': form})
