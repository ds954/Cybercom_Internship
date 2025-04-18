from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','due_date','complete']
       