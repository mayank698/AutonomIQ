from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successfull")
            return redirect("login")
        else:
            context = {"form": form}
            return render(request, "register.html", context)
    else:
        form = RegisterForm()
        context = {"form": form}
    return render(request, "register.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")
    else:
        form = AuthenticationForm()
        context = {"form": form}
    return render(request, "login.html", context)


def logout(request):
    auth.logout(request)
    return redirect("home")
