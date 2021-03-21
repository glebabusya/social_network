from django import forms
from django.core import exceptions
from .models import Group
from registration.models import Account


class GroupForm(forms.ModelForm):
    queryset = Group.objects.get().subscribers.all()
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'profile-input'}))
    # special inputs
    current_info = forms.CharField(required=True,
                                   widget=forms.Textarea(
                                       attrs={'class': 'profile-input current-info-input', 'rows': "10", 'cols': '10'}))

    short_name = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': 'profile-input'}))

    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'profile-input'}))

    closed = forms.CheckboxInput(attrs={'class': 'profile-input'})

    admin = forms.ModelChoiceField(queryset=queryset, empty_label=None, )

    class Meta:
        model = Group
        fields = [
            'title',
            'current_info',
            'short_name',
            'avatar',
            'closed',
            'admin'
        ]
