from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm
from django import forms
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CreateBountyPostForm(ModelForm):
    class Meta:
        model = BountyPost
        fields = '__all__'