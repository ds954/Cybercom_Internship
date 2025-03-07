from django.db import models
from django.contrib.auth.hashers import make_password

class UserInfo(models.Model):
    Username=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    email_otp=models.CharField(max_length=6,null=False,blank=False)
    password=models.CharField(max_length=255)
    firstname=models.CharField(max_length=200,blank=True)
    lastname=models.CharField(max_length=200,blank=True)
    phone=models.CharField(max_length=10,blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Username

class RefreshTokenStore(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="refresh_tokens")
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.token[:10]}..."