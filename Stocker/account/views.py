from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# Create your views here.

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:home_view')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'account/login.html', context)



def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home_view')
    else:
        form = RegisterForm()
    context = {'form':form}
    return render(request, 'account/register.html', context)



def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, 'Succssfully logout')
    return redirect('main:home_view')