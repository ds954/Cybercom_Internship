# library/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BorrowRequest, Book
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime

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