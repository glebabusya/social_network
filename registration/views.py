from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms, models
from django.contrib import messages


class RegistrationView(View):
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

        if password == password_confirm:
            try:
                user = get_user_model().objects.create_user(first_name=first_name,
                                                            last_name=last_name,
                                                            username=username,
                                                            email=email,
                                                            birthday=birthday,
                                                            password=password)
                user.save()
                return redirect('home')  # redirect to user profile
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
                email=data['email'],
                password=data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('home')  # regirect to user profile
            else:
                messages.error(request, 'Incorrect password')
        return redirect('login')
