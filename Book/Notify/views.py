from django.shortcuts import render
from .models import Book
from django.utils import timezone
from .tasks import send_due_date_notifications
from django.contrib.auth.models import User

def notifications(request):
    """Triggers Celery task and returns due books for the user."""

    user = User.objects.get(username="dhara") 
    print(user)
    # send_due_date_notifications.delay(user.id)
    send_due_date_notifications(user.id,repeat=60)
    print(f"Task sent for user: {user.id}")
    today = timezone.now().date()
    due_books = Book.objects.filter(user=user, due_date=today + timezone.timedelta(days=3))
    
    return render(request, "notifications.html", {"due_books": due_books})
