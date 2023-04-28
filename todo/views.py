from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'todo/sign_up_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo/sign_up_user.html',
                              {'form': UserCreationForm(),
                               'error': 'This username already exists. Please select a new username'})
        else:
            return render(request, 'todo/sign_up_user.html',
                          {'form': UserCreationForm(), 'error': 'Passwords didnt match'})


def current_todos(request):
    return render(request, 'todo/current_todos.html', {'form': UserCreationForm()})