from django import forms
from .models import UserInfo

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['profile_picture']
class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['Username', 'email', 'firstname', 'lastname', 'phone', 'profile_picture']