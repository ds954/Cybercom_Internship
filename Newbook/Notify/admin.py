from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import BorrowRequest, Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

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
        return obj.status
    
    action_buttons.short_description = "Actions"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('accept/<int:request_id>/', self.accept_request, name='accept_request'),
            path('reject/<int:request_id>/', self.reject_request, name='reject_request'),
            path('accept_renewal/<int:request_id>/', self.accept_renewal, name='accept_renewal'),
            path('reject_renewal/<int:request_id>/', self.reject_renewal, name='reject_renewal'),
            
        ]
        return custom_urls + urls

    def accept_request(self, request, request_id):
        return self.update_status(request, request_id, "accepted")

    def reject_request(self, request, request_id):
        return self.update_status(request, request_id, "rejected")
    def accept_renewal(self, request, request_id):
        return self.update_status(request, request_id, "renew_accpect")  
    def reject_renewal(self, request, request_id):
        return self.update_status(request, request_id, "renew_reject")
    
    def update_status(self, request, request_id, status):
        borrow_request = BorrowRequest.objects.get(id=request_id)
        borrow_request.status = status
        borrow_request.save()

        # Send real-time notification to user
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{borrow_request.user.id}",
            {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
        )

        messages.success(request, f"Request {status} successfully!")
        return redirect('/admin/Notify/borrowrequest/')