from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django import forms

from .models import ToDo


class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'important']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = AbstractUser
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = AbstractUser
        fields = ['username', 'password1', 'password2']
