from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.



def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        new_user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
        new_user.save()
        login(request, new_user)
        messages.success(request, 'Jouin successfully, Welcome')
        return redirect('main:home_view')
    return render(request, 'account/register.html')



def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            messages.success(request, 'Jouin successfully, Welcome')
            return redirect('main:home_view')
        else:
            messages.error(request, 'username or password is wrong please try agine!')
    return render(request, 'account/login.html')



def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, 'Succssfully logout')
    return redirect('main:home_view')