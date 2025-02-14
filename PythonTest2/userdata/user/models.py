from django.db import models

class Userinfo(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Plain text password
    email_otp = models.CharField(max_length=6, null=True, blank=True)  # OTP can be null after verification
    is_email_verified = models.BooleanField(default=False)  # Flag to check email verification status
