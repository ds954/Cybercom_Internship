from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import BorrowRequest, Book
from django.core.mail import send_mail
from djangoauthapi import settings
from datetime import timezone
from .models import CustomUser

admin.site.register(CustomUser)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','is_available']

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
        book = borrow_request.book #get correct book
        book.is_available = False
        book.save()
        return self.update_status(request, request_id, "accepted")

    def reject_request(self, request, request_id):
        return self.update_status(request, request_id, "rejected")
    def accept_renewal(self, request, request_id):
        return self.update_status(request, request_id, "renew_accpect")  
    def reject_renewal(self, request, request_id):
        return self.update_status(request, request_id, "renew_reject")
    def cancel_request(self,request,request_id):
        return self.update_status(request,request_id,'Cancel_Request')
    def book_returned(self,request,request_id):
        borrow_request = BorrowRequest.objects.get(id=request_id)
        book = borrow_request.book
        book.is_available = True 
        book.save() 
        return self.update_status(request,request_id,'book_returned')
    
    def update_status(self, request, request_id, status):
        print(f"Updating status to {status} for request {request_id}")  # Debugging
        borrow_request = BorrowRequest.objects.get(id=request_id)
        borrow_request.status = status
        borrow_request.save()

        book = borrow_request.book #get correct book
        if status in ["accepted", "renew_accpect"]:
            book.is_available = False
        # if borrow_request.Duedate and borrow_request.Duedate < timezone.now().date() and status == "renew_accpect" or status == "accepted":
        #     book.is_available = True
        elif status in ["book_returned", "rejected"]:
            book.is_available = True 
        book.save()

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
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,  
        #     [borrow_request.user.email],  
        #     fail_silently=False,
        # )

        # Send real-time notification to user
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     f"user_{borrow_request.user.id}",
        #     {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
        # )
        print("see message")
        messages.success(request, f"Request {status} successfully!")
        return redirect('/admin/account/borrowrequest/')
        