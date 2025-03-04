from django.contrib import admin
from .models import RefreshTokenModel
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import BorrowRequest, Book,BookCopy
from django.core.mail import send_mail
from djangoauthapi import settings
from datetime import timezone

# Register your models here.
admin.site.register(RefreshTokenModel)


@admin.register(BookCopy)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'book','copy_number','is_borrowed','borrowed_by']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','is_available','quantity']
    def save_model(self, request, obj, form, change):
        """Overrides save_model to create BookCopy records when a new Book is added."""
        is_new = obj.pk is None  # Check if the book is new
        super().save_model(request, obj, form, change)  # Save the book first

        if is_new:  # If it's a new book, create copies
            book_copies = [BookCopy(book=obj, copy_number=i) for i in range(1, obj.quantity + 1)]
            BookCopy.objects.bulk_create(book_copies)  # Bulk insert for efficiency

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'book','IssuedDate','Duedate', 'status', 'action_buttons')

    def action_buttons(self, obj):
        if obj.status == "pending":
            return format_html(
                '<a class="button" href="accept/{}/">Accept</a>&nbsp;'
                '<a class="button" href="reject/{}/">Reject</a>',
                obj.id, obj.id
            )
        elif obj.status=='renewal_requested':
            return format_html(
                '<a class="button" href="accept_renewal/{}/">Renewal Req Accept</a>&nbsp;'
                '<a class="button" href="reject_renewal/{}/">Renewal Req Reject</a>',
                obj.id, obj.id
            )
        elif obj.status == "renew_accpect":
            return "Renewal Accepted" 
        elif obj.status == "renew_reject":
            return "Renewal Rejected"
        elif obj.status == "Cancel_Request":
            return "Request Canceled"
        elif obj.status=="book_returned":
            return "book_returned"
        return obj.status
    
    action_buttons.short_description = "Actions"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('accept/<int:request_id>/', self.accept_request, name='accept_request'),
            path('reject/<int:request_id>/', self.reject_request, name='reject_request'),
            path('accept_renewal/<int:request_id>/', self.accept_renewal, name='accept_renewal'),
            path('reject_renewal/<int:request_id>/', self.reject_renewal, name='reject_renewal'),
            path('cancel_request/<int:request_id>/',self.cancel_request, name="cancel_request"),
            path('book_returned/<int:request_id>/',self.book_returned, name="book_returned"),
            
        ]
        return custom_urls + urls

    def accept_request(self, request, request_id):
        borrow_request = BorrowRequest.objects.get(id=request_id)
        book = borrow_request.book 

        available_copy = BookCopy.objects.filter(book=book, is_borrowed=False).first()
        if available_copy:
            available_copy.is_borrowed = True
            available_copy.borrowed_by = borrow_request.user  
            available_copy.save()
        borrow_request.book_copy = available_copy
        borrow_request.save()
        if book.quantity > 0:  
            book.is_available=True
            book.quantity -= 1
        if book.quantity == 0:
            book.is_available = False
        book.save()
        return self.update_status(request, request_id, "accepted")

    def reject_request(self, request, request_id):
        return self.update_status(request, request_id, "rejected")
    def accept_renewal(self, request, request_id):
        return self.update_status(request, request_id, "renew_accpect")  
    def reject_renewal(self, request, request_id):
        borrow_request = BorrowRequest.objects.get(id=request_id)
        book = borrow_request.book
        book.quantity += 1
        book.is_available = True 
        book.save()
        return self.update_status(request, request_id, "renew_reject")
    def cancel_request(self,request,request_id):
        return self.update_status(request,request_id,'Cancel_Request')
    def book_returned(self,request,request_id):
        borrow_request = BorrowRequest.objects.get(id=request_id)
        book = borrow_request.book
        return self.update_status(request,request_id,'book_returned')
    
    def update_status(self, request, request_id, status):
        print(f"Updating status to {status} for request {request_id}")  # Debugging
        borrow_request = BorrowRequest.objects.get(id=request_id)
        borrow_request.status = status
        borrow_request.save()

        book = borrow_request.book #get correct book
        # if status in ["accepted", "renew_accpect"]:
        #     book.is_available = False
        # if borrow_request.Duedate and borrow_request.Duedate < timezone.now().date() and status == "renew_accpect" or status == "accepted":
        #     book.is_available = True
        # elif status in ["book_returned", "rejected","renew_reject"]:
        #     book.is_available = True 
        book.save()
        print(f"Updating status to {status}: Quantity={book.quantity}, is_available={book.is_available}")


        subject = "Library Borrow Request Update"
        if status == "accepted":
            message = f"Your borrow request for '{borrow_request.book.title}' has been accepted."
        elif status == "rejected":
            message = f"Unfortunately, your borrow request for '{borrow_request.book.title}' has been rejected."
        elif status == "renew_accpect":
            message = f"Your renewal request for '{borrow_request.book.title}' has been accepted."
        elif status == "renew_reject":
            message = f"Your renewal request for '{borrow_request.book.title}' has been rejected."
        elif status == 'Cancel_Request':
            message = f"You Cancel '{borrow_request.book.title}'."
        elif status == 'book_returned':
            message = f"You returned '{borrow_request.book.title}'."


        print('Sending mail')
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  
            [borrow_request.user.email],  
            fail_silently=False,
        )

        # Send real-time notification to user
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{borrow_request.user.id}",
            {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
        )
        print("see message")
        messages.success(request, f"Request {status} successfully!")
        return redirect('/admin/app/borrowrequest/')
        