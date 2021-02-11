from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account
from django.core import exceptions


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'email')


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('username', 'email')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input1', 'placeholder': 'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input1', 'placeholder': 'Password'}),
                               label='')
