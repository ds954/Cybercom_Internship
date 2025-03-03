from django.db import models
from django.contrib.auth.models import User

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField( max_length=30,choices=STATUS_CHOICES, default='pending')
    IssuedDate=models.DateField(null=True)
    Duedate=models.DateField(null=True)
    


    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.status}"
