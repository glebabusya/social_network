from django import forms
from django.core import exceptions
from registration.models import Account


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(disabled=True, required=False,
                                 widget=forms.TextInput(attrs={'class': 'profile-input'}))
    last_name = forms.CharField(disabled=True, required=False,
                                widget=forms.TextInput(attrs={'class': 'profile-input'}))

    gender = forms.ChoiceField(disabled=True, required=False, choices=[('Male', 'Male'), ('Female', 'Female')],
                               widget=forms.TextInput(attrs={'class': 'profile-input'}))

    username = forms.CharField(disabled=True, required=False,
                               widget=forms.TextInput(attrs={'class': 'profile-input'}))

    email = forms.CharField(disabled=True, required=False,
                            widget=forms.TextInput(attrs={'class': 'profile-input'}))

    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'profile-input'}))

    birthday = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'profile-input'}))

    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'profile-input'}))

    work = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'profile-input'}))

    study = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'profile-input'}))

    # special inputs
    current_info = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'profile-input current-info-input'}))

    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'profile-input'}))

    closed = forms.CheckboxInput(attrs={'class': 'profile-input'})

    can_comment = forms.CheckboxInput(attrs={'class': 'profile-input'})

    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'gender',
            'username',
            'email',
            'phone_number',
            'birthday',
            'city',
            'work',
            'study',
            'current_info',
            'closed',
            'can_comment',
        ]

        labels = {
            'closed': 'Can other people watch info from your page',
            'can_comment': 'Can other people comment yout notes'
        }
