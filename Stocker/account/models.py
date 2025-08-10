from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
