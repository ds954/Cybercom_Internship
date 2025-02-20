from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import BorrowRequest

# User Requests a Book
def user_borrow_request(request):
    borrow_requests = BorrowRequest.objects.filter(user=request.user)

    if request.method == "POST":
        book_title = request.POST.get("book_title").strip()
        if book_title:  # Ensure book title is not empty
            borrow_request = BorrowRequest(user=request.user, book_title=book_title)
            borrow_request.save()

            # Notify Admin via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "borrow_requests",
                {"type": "update_request", "message": f"New borrow request: {book_title}"}
            )

    return render(request, "user_borrow.html", {"borrow_requests": borrow_requests})


# Admin Updates the Request Status
def update_request_status(request, request_id, action):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)

    if action == "accept":
        borrow_request.status = "Accepted"
    elif action == "reject":
        borrow_request.status = "Rejected"
    
    borrow_request.save()

    # Notify the user via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "borrow_requests",
        {"type": "update_request", "message": f"Request for '{borrow_request.book_title}' is now {borrow_request.status}"}
    )

    return JsonResponse({"status": borrow_request.status})  # Return updated status
