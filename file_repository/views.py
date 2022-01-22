from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import CustomUserForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import EmailBackend
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the file_repo index.")


def register_request(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form['email'].value()).exists():
                messages.error(
                    request, "Unsuccessful registration. Email already exists.")
            else:
                form.save()
                messages.success(request, "Registration successful.")
            # return redirect('file_repository:index') #remove else if u got something here
        else:
            messages.error(
                request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserForm()
    return render(request=request, template_name="file_repository/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        username = form['username'].value()
        password = form['password'].value()
        user1 = authenticate(username=username, password=password)
        user2 = EmailBackend.authenticate(request, username, password)
        user = user1 if user1 != None else user2
        if user is not None:
            login(request, user)
            messages.info(
                request, f"You are now logged in as {user}.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, "file_repository/login.html", {"login_form": form})


def logout_request(request):
    logout(request)
    return redirect('file_repository:index')
