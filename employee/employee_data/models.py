from django.db import models
from django import forms  
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

class StudentForm(forms.Form):  
    firstname = forms.CharField(label="Enter first name",max_length=50)  
    lastname  = forms.CharField(label="Enter last name", max_length = 100)
    email     =forms.EmailField(label="enter email")
    file      = forms.FileField()
  



class CustomUserManager(BaseUserManager):
    """Manager for CustomUser"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Remove username field from default User model
    email = models.EmailField(unique=True)  # Use email as the primary field
    email_otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = "email"  # Login via email instead of username
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Fields required for user creation

    objects = CustomUserManager()  # Assign custom manager

    def __str__(self):
        return self.email




