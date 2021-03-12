from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, "todo/home.html")


def currenttodos(request):
    return render(request, "todo/currenttodos.html")


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
            return redirect('home')

    context["form"] = AuthenticationForm()
    return render(request, 'todo/login.html', context=context)


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
