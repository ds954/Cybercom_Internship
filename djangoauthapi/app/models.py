from django.db import models
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class RefreshTokenModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(unique=True)  # Store the refresh token
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Store token expiry

    def __str__(self):
        return f"Token for {self.user.email} (expires {self.expires_at})"

    @classmethod
    def create_token(cls, user):
        """Generates and stores a refresh token for the user"""
        refresh = RefreshToken.for_user(user)
        return cls.objects.create(
            user=user, 
            token=str(refresh), 
            expires_at=refresh.payload["exp"]
        )
