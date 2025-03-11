from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta

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
    
class Book(models.Model):
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    is_available= models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    copy_number = models.PositiveIntegerField()  
    is_borrowed = models.BooleanField(default=False)
    borrowed_by = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, blank=True)

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

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField( max_length=30,choices=STATUS_CHOICES, default='pending')
    IssuedDate=models.DateField(null=True)
    
    def get_due_date():
        return timezone.now().date() + timedelta(days=60)
    Duedate=models.DateField(default=get_due_date())


    def __str__(self):
        return f"{self.user.Username} - {self.book.title} - {self.status}"

