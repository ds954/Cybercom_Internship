from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BorrowRequest, Book
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .admin import BorrowRequestAdmin
from django.contrib import admin


def search(request):
    return render(request, 'user_dashboard.html')

def search_results(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type')
    results = []
    searched = False

    if query:
        searched = True;
        if search_type == 'title':
            results = Book.objects.filter(title__icontains=query)
        elif search_type == 'author':
            results = Book.objects.filter(author__icontains=query)
        elif search_type == 'category':
            results = Book.objects.filter(category__icontains=query)

    return render(request, 'user_dashboard.html', {'results': results, 'searched': searched})
@login_required
def user_dashboard(request):
    borrow_requests = BorrowRequest.objects.filter(user=request.user)
    books = Book.objects.all()
    today=datetime.now().date()
    return render(request, 'user_dashboard.html', {'borrow_requests': borrow_requests, 'books': books,'today':today})

@login_required
def request_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        BorrowRequest.objects.create(user=request.user, book=book)
        return redirect('user_dashboard')
    else:
        return redirect('user_dashboard')
    
@login_required
def request_renewal(request,request_id):
    borrow_request = BorrowRequest.objects.get(id=request_id)
    borrow_request.status = 'renewal_requested'
    borrow_request.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{borrow_request.user.id}",
        {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
    )
    return redirect('user_dashboard')   

@login_required
def cancel_book(request,request_id):
     print(f"Cancelling request {request_id}") 
     cancel_request=BorrowRequest.objects.get(id=request_id)
     cancel_request.status='Cancel_Request'
     cancel_request.save()

     channel_layer=get_channel_layer()
     async_to_sync(channel_layer.group_send)(
          f"user_{cancel_request.user.id}",
         {"type":"cancel_request","status":cancel_request.status, "book":cancel_request.book.title}
     )

     subject = "Library Borrow Request Canceled"
     message = f"Your borrow request for '{cancel_request.book. title}' has been canceled."
     recipient_email = cancel_request.user.email  
        
     send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

        # Display message on the screen
     messages.success(request, f"Borrow request for '{cancel_request.book.title}' has been canceled successfully.")

     return redirect('user_dashboard')

@login_required
def return_book(request,request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id, user=request.user)
    borrow_request.status = 'book_returned'
    borrow_request.save()
    book=borrow_request.book
    print(f"Before return: Quantity={book.quantity}, is_available={book.is_available}")
    book.quantity += 1  
    book.is_available = True  
    book.save() 
    print(f"After return: Quantity={book.quantity}, is_available={book.is_available}")

    from .admin import BorrowRequestAdmin
    admin_instance = BorrowRequestAdmin(BorrowRequest, admin.site)
    admin_instance.update_status(request, request_id, 'book_returned')

    

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{borrow_request.user.id}",
        {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
    )
    messages.success(request, f"You have successfully returned '{borrow_request.book.title}' book.")

    return redirect('user_dashboard')