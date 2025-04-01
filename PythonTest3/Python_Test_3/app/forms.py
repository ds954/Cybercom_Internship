from django import forms
from .models import EmployeeProfile

class EmployeeForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=100)
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@xyz.com'):
            raise forms.ValidationError("Email must be from @xyz.com domain.")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['Employee','profile_picture']

class UserForm(forms.Form):
    name=forms.CharField(max_length=100,required=True)
    email=forms.EmailField()
    joined_date=forms.DateField()
    Designation=forms.CharField(max_length=255)

