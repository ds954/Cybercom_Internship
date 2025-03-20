from django.contrib import admin
from .models import UserInfo, Book, BookCopy,BorrowRequest,Notification,RefreshTokenStore,RenewalRequests,AdminActions
from import_export.admin import ImportExportModelAdmin
from .resources import BookResource
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.core.mail import send_mail
from Library_Management_System import settings
from datetime import timezone,datetime,timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse


from django.contrib.admin import AdminSite
from django.template.loader import render_to_string
from django.http import HttpResponse

class CustomAdminSite(AdminSite):

    def index(self, request, extra_context=None):
        """Render default Django Admin index page using render_to_string()"""
        extra_context = extra_context or {}
        extra_context['user_id'] = request.user.id  

        html_content = render_to_string('admin/index.html', extra_context, request=request)
        return HttpResponse(html_content)

    def login(self, request, extra_context=None):
        """Render default Django Admin login page using render_to_string()"""
        extra_context = extra_context or {}
        html_content = render_to_string('admin/login.html', extra_context, request=request)
        return HttpResponse(html_content)

    def logout(self, request, extra_context=None):
        """Render default Django Admin logout page using render_to_string()"""
        extra_context = extra_context or {}
        html_content = render_to_string('admin/logout.html', extra_context, request=request)
        return HttpResponse(html_content)

custom_admin_site = CustomAdminSite(name="custom_admin")

# Register your models




@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'Username', 'email','firstname','lastname','phone']

admin.site.register(Notification)
admin.site.register(RefreshTokenStore)

@admin.register(RenewalRequests)
class RenewalRequestsAdmin(admin.ModelAdmin):
    list_display = ('borrow_id', 'admin_id', 'created_at', 'updated_at', 'current_status')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('borrow_id__user__Username', 'borrow_id__book__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AdminActions)
class AdminActionsAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'action_type', 'timestamp')

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'copy_number', 'is_borrowed', 'borrowed_by']


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    """
    Django Admin for Book with import-export functionality.
    Automatically creates BookCopy records when a new Book is added.
    """
    resource_class = BookResource
    list_display = ("id", "title", "author", "category", "is_available", "quantity")
    search_fields = ("title", "author", "category")

    # 
    # In BookAdmin (admin.py)

def save_model(self, request, obj, form, change):
    super().save_model(request, obj, form, change)
    if not change:
        AdminActions.objects.create(
            admin_id=request.user,
            action_type="Add Book",
            description=f"Added book: {obj.title}"
        )
        book_copies = [
            BookCopy(book=obj, copy_number=i) for i in range(1, obj.quantity + 1)
        ]
        BookCopy.objects.bulk_create(book_copies)
    else:
        AdminActions.objects.create(
            admin_id=request.user,
            action_type="Edit Book",
            description=f"Edited book: {obj.title}"
        )

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
        userinfo_user = borrow_request.user 
        available_copy = BookCopy.objects.filter(book=book, is_borrowed=False).first()
        if available_copy:
            available_copy.is_borrowed = True
            available_copy.borrowed_by = userinfo_user 
            available_copy.save()
            
        borrow_request.book_copy = available_copy
        
        borrow_request.save()
        if book.quantity > 0:  
            book.is_available=True
            book.quantity -= 1
        if book.quantity == 0:
            book.is_available = False
        book.save()
        AdminActions.objects.create(
        admin_id=request.user,
        action_type="Approve Borrow Request",
        description=f"Approved request for {borrow_request.book.title} and user is {borrow_request.user.Username}"
        )
        return self.update_status(request, request_id, "accepted")

    def reject_request(self, request, request_id):
        borrow_request = BorrowRequest.objects.get(id=request_id)
        AdminActions.objects.create(
            admin_id=request.user,
            action_type="Reject Borrow Request",
            description=f"Rejected request for {borrow_request.book.title} and user is {borrow_request.user.Username}"
        )
        return self.update_status(request, request_id, "rejected")
    def accept_renewal(self, request, request_id):
        borrow_request = BorrowRequest.objects.get(id=request_id)

        # Update status directly on BorrowRequest
        borrow_request.status = 'renew_accpect'
        borrow_request.Duedate = datetime.now().date() + timedelta(days=60)
        borrow_request.save()
        
        AdminActions.objects.create(
        admin_id=request.user,
        action_type="Approve Renewal Request",
        description=f"Approved renewal for {borrow_request.book.title} and user is {borrow_request.user.Username}"
        )
        return self.update_status(request, request_id, "renew_accpect")  
    def reject_renewal(self, request, request_id):
        borrow_request = BorrowRequest.objects.get(id=request_id)

        borrow_request.status = 'renew_reject'
        borrow_request.save()
        
        book = borrow_request.book
        book.quantity += 1
        book.is_available = True 
        book.save()
        AdminActions.objects.create(
        admin_id=request.user,
        action_type="Reject Renewal Request",
        description=f"Rejected renewal for {borrow_request.book.title} and user is {borrow_request.user.Username}"
        )
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

        book = borrow_request.book 
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
        Notification.objects.create(
        user=borrow_request.user,
        message=message
        )
        # Send real-time notification to user
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{borrow_request.user.id}",
            {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title,"message": message}
        )
        print("see message")
        messages.success(request, f"Request {status} successfully!")
        messages.success(request, message)

        
        # return redirect('user_notifications')
        return redirect('/admin/app/borrowrequest/')
    
