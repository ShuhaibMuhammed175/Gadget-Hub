from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class user_creation(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password Again'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
