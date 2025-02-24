from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Book
from django.contrib.auth.models import User
from background_task import background

# @shared_task
@background(schedule=30)
def send_due_date_notifications(user_id):
    print(user_id)
    print(type(user_id))
    user = User.objects.get(id=user_id)
    
    today = timezone.now().date()
    three_days_later = today + timezone.timedelta(days=3)

    due_soon_books = Book.objects.filter(user=user, due_date=three_days_later)

    print(f"today's Date: {today}")
    print(f"Three Days Later: {three_days_later}")
    print(f"Matching Books: {list(due_soon_books.values('book_title', 'due_date'))}")  

    if due_soon_books.exists():
        print("Found books due in 3 days!")
        for book in due_soon_books:
            message = f"Reminder: {book.book_title} is due in 3 days!"
            print(f"Sending notification for: {book.book_title}")


            # Send Email notification
            send_mail(
                "Book Due Reminder",
                message,
                settings.EMAIL_HOST_USER,
                [book.user.email],  
                fail_silently=False,
            )
            
            print(f"Email sent to {book.user.email}")
            # Send WebSocket notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications", {"type": "send_notification", "message": message}
            )
            print(f"WebSocket notification sent for {book.book_title}")
    else:
        print("No books due in 3 days! This should not happen.")
