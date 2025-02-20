from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class Book(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    issued_date = models.DateField(auto_now_add=True) #set to the current date and time  when a new book record is added to the database.
    due_date = models.DateField()

    def is_due_soon(self):
        """Check if the due date is exactly 3 days away."""
        return self.due_date == (timezone.now().date() + timezone.timedelta(days=3))#calculates the date that is exactly three days from the current date.
    def __str__(self):
        return f"{self.book_title} - Due on {self.due_date}"
