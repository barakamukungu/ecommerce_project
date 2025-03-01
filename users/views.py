from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("store:home")  # Redirect to homepage
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("store:home")  # Redirect to homepage
