from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from todo.forms import TodoForm
from todo.models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "todo/home.html")


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    context = {
        "todos": todos
    }
    return render(request, "todo/currenttodos.html", context=context)


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False)
    context = {
        "todos": todos
    }
    return render(request, "todo/completed-todos.html", context=context)


def signupuser(request):
    context = {
    }

    if request.method == "POST":
        # fetch user data
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if (password1 == password2):
            # Create a new user
            try:
                user = User.objects.create_user(
                    username=username, password=password1)
                user.save()
                login(request, user=user)
                return redirect('currenttodos')
            except IntegrityError:
                context["error"] = "That username has already been taken. Please choose a new username"
        else:
            context["error"] = "Password does not match."
    context["form"] = UserCreationForm()
    return render(request, 'todo/signup.html', context=context)


def loginuser(request):
    context = {
    }
    if request.method == "POST":
        # check user is authenticate or not
        user = authenticate(
            request=request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            context["error"] = "Password does not match."
        else:
            login(request, user=user)
            return redirect('currenttodos')

    context["form"] = AuthenticationForm()
    return render(request, 'todo/login.html', context=context)


@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


@login_required
def create_todo(request):
    context = {}
    if request.method == "POST":
        try:
            todo = TodoForm(request.POST)
            new_todo = todo.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except Exception:
            context["error"] = "Something bad happen. Please try again"

    context["form"] = TodoForm()
    return render(request, "todo/create-todo.html", context=context)


@login_required
def view_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    context = {
        "todo": todo
    }
    if request.method == "POST":
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except Exception:
            context["error"] = "Something bad happen. Please try again"
    context["form"] = TodoForm(instance=todo)
    return render(request, "todo/view-todo.html", context=context)


@login_required
def completed_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodos')
