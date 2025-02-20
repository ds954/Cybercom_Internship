from django.db import models
from django.contrib.auth.models import User

class BorrowRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book_title=models.CharField(max_length=200)
    status=models.CharField(
        max_length=10,
        choices=[('pending','pending'),('accept','accept'),('reject','reject')],
        default='pending',
    )
    request_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book_title} ({self.status})"

