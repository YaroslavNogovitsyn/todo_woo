from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo


def home(request):
    return render(request, 'todo/home.html', {'title': 'Home'})


def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'todo/sign_up_user.html', {'form': UserCreationForm(), 'title': 'Sign Up'})
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
                               'error': 'This username already exists. Please select a new username',
                               'title': 'Sign Up'})
        else:
            return render(request, 'todo/sign_up_user.html',
                          {'form': UserCreationForm(), 'error': 'Passwords didnt match', 'title': 'Sign Up'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm(), 'title': 'Login'})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match',
                           'title': 'Sign Up'})
        else:
            login(request, user)
            return redirect('current_todos')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html',
                      {'form': ToDoForm(), 'title': 'Create ToDo'})
    else:
        try:
            form = ToDoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('home')
        except ValueError:
            return render(request, 'todo/create_todo.html',
                          {'form': ToDoForm(), 'title': 'Create ToDo', 'error': 'Bad data passed in. Try again'})


def current_todos(request):
    todos = ToDo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/current_todos.html', {'title': 'Current ToDos', 'todos': todos})


def view_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        return render(request, 'todo/view_todo.html', {'title': f'ToDo №{todo_pk}', 'todo': todo, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            form = ToDoForm(instance=todo)
            return render(request, 'todo/view_todo.html',
                          {'title': f'ToDo №{todo_pk}', 'todo': todo, 'form': form, 'error': 'Bad info. Try again'})