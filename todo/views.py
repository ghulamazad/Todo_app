from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login


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
    return render(request, 'todo/signupuser.html', context=context)


def currenttodos(request):
    return render(request, "todo/currenttodos.html")
