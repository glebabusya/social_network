import random

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms, models
from django.contrib import messages


def generate_hash_url(user):
    symbols = 'abcdefghjklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ0123456789'
    username = user.username
    name = user.first_name
    url = ''
    username_half1 = username[:(len(username) // 2)]
    username_half2 = username[(len(username) // 2):]
    for letter in username_half1[::-1]:
        url += random.choice(symbols) + random.choice(symbols)
        url += letter

    url += random.choice(symbols) + random.choice(symbols)

    for letter in username_half2[::-1]:
        url += letter
        url += random.choice(symbols) + random.choice(symbols)

    name_half1 = name[:(len(name) // 2)]
    name_half2 = name[(len(name) // 2):]

    url += '-'

    for letter in name_half1[::-1]:
        url += random.choice(symbols) + random.choice(symbols)
        url += letter

    url += random.choice(symbols) + random.choice(symbols)

    for letter in name_half2[::-1]:
        url += letter
        url += random.choice(symbols) + random.choice(symbols)

    url += '-'

    while len(url) <= 200:
        url += random.choice(symbols + '-')

    return url


def decrypt(url):
    username_hash, name_hash, *garbage = url.split('-')
    username_hash = username_hash[2:][:-2][::3]
    name_hash = name_hash[2:][:-2][::3]

    username_half1 = username_hash[:(len(username_hash) // 2)]
    username_half2 = username_hash[(len(username_hash) // 2):]

    username = ''
    for letter in username_half1[::-1]:
        username += letter

    for letter in username_half2[::-1]:
        username += letter

    name_half1 = name_hash[:(len(name_hash) // 2)]
    name_half2 = name_hash[(len(name_hash) // 2):]

    name = ''
    for letter in name_half1[::-1]:
        name += letter

    for letter in name_half2[::-1]:
        name += letter

    return username, name


class RegistrationView(View):
    symbols = '''
                !@#$%^&*()_+=-,./?><|\\"'`~№;%: 
            '''

    def get(self, request):
        context = {}
        return render(request, 'registration/registration.html', context)

    def post(self, request):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')
        birthday = request.POST.get('birthday')

        for symbol in self.symbols:
            if symbol in username:
                messages.error(request, 'Create a unique user')
                return redirect('registration')

        if password == password_confirm:
            try:
                user = get_user_model().objects.create_user(first_name=first_name,
                                                            last_name=last_name,
                                                            username=username,
                                                            email=email,
                                                            birthday=birthday,
                                                            password=password)
                user.save()
                return redirect('profile', user)  # redirect to user profile
            except IntegrityError:
                messages.error(request, 'Create a unique user')
        else:
            messages.error(request, 'Incorrect password')
        return redirect('registration')


class LoginView(View):
    def get(self, request):
        logout(request)
        form = forms.LoginForm()
        context = {'form': form}
        return render(request, 'registration/login.html', context)

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('profile', user.username)  # redirect to user profile
            else:
                messages.error(request, 'Incorrect password')
        return redirect('login')


class AccountRecoveryView(View):
    def get(self, request):
        return render(request, 'registration/recovery.html')

    def post(self, request):
        username = request.POST.get('username')
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            messages.error(request, 'No such user')
            return render(request, 'registration/recovery.html')

        send_mail('bot', '123123', 'glebabusya@mail.ru', [user.email],
                  html_message=f'<a href="http://127.0.0.1:8000/news/password-change{generate_hash_url(user)}">qweqwe</a>')

        return redirect('login')


class ChangePasswordView(View):
    def get(self, request, hash):
        return render(request, 'registration/password_change.html')

    def post(self, request, hash):
        username, name = decrypt(hash)

        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')

        if password == password_confirm:
            try:
                user = get_user_model().objects.get(username=username, first_name=name)
                user.set_password(password)
                user.save()
            except get_user_model().DoesNotExist:
                pass
            return redirect('login')

        messages.error(request, 'incorrect password')
        return redirect('password-change', hash)
