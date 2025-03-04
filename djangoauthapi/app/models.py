from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils.timezone import now
from account.models import CustomUser

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
        expires_at = now() + timedelta(days=7)  # Default JWT refresh token expiry
        return cls.objects.create(
            user=user,
            token=str(refresh),
            expires_at=expires_at
        )

class Book(models.Model):
    title = models.CharField(max_length=255)
    is_available=models.BooleanField(default=True)
    quantity=models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.title
    
class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    copy_number = models.PositiveIntegerField()  
    is_borrowed = models.BooleanField(default=False)
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"

class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('renewal_requested', 'Renewal Requested'),
        ('renew_accpect','Renewal Request accepted'),
        ('renew_reject','Renewal Request rejected'),
        ('Cancel_Request',"Request Cancel"),
        ('book_returned',"return"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='app_borrow_requests')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField( max_length=30,choices=STATUS_CHOICES, default='pending')
    IssuedDate=models.DateField(null=True)
    Duedate=models.DateField(null=True)
    


    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.status}"
