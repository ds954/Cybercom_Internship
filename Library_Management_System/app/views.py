from django.contrib.auth.decorators import login_required
from django.db.models import Q  
import os
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
from app.OtpGenration import generate_otp,verifyotp
from .models import UserInfo
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Book,BorrowRequest,Notification,RefreshTokenStore,RenewalRequests,AdminActions,MemberActivity
from .admin import BorrowRequestAdmin
from .forms import ProfileForm,UserForm,BookForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages
from django.contrib import admin
from django.utils import timezone
from app.decoraters import session_login_required
from django.contrib.auth.decorators import login_required
from .tasks import send_due_date_notifications
from datetime import datetime,timedelta
import jwt
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication
from django.http import JsonResponse
import time
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages import get_messages
from .forms import BookBulkUploadForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from .models import BorrowRequest, UserInfo, Notification
from django.utils.timezone import now
from django.contrib.auth.models import User
from app.context_processors import user_context_processor
from django.http import HttpResponseRedirect
from reportlab.lib.pagesizes import landscape, A3
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .admin import BookAdmin
from reportlab.platypus import SimpleDocTemplate
from django.db.models import Count

def admin_profile_view(request):
    """
    Display the admin profile page.

    Args:
        request (HttpRequest): The incoming request from the client.

    Returns:
        HttpResponse: Rendered admin profile HTML page.
    """
    user = request.user  
    admin_profile = User.objects.get(username=user)  

    html_content=render_to_string('admin/admin_profile.html', {'admin_profile': admin_profile})
    return HttpResponse(html_content)

@csrf_exempt
def admin_profile_edit(request):
    """
    Handle admin profile editing.

    On POST request, updates the admin's profile details.
    On GET request, renders the profile edit form.

    Args:
        request (HttpRequest): The incoming request from the client.

    Returns:
        HttpResponse: Redirects after update or renders edit form.
    """
    user = request.user  # Get the logged-in admin user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Update user information
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('admin_profile')  # Redirect to profile view after update
    html_content=render_to_string('admin/admin_profile_edit.html', {'admin_profile': user})
    return HttpResponse(html_content)

def borrowed_books_report(request):
    """
    Generate a report of all currently borrowed books, most borrowed book,
    and user borrowing statistics.

    Args:
        request (HttpRequest): The incoming request from the client.

    Returns:
        HttpResponse: Rendered HTML page for borrowed books report.
    """
    today=datetime.now().date()
    borrowed_books = BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect','renewal_requested'])
    admin_data=AdminActions.objects.all()
    user_borrow_stats = (
        UserInfo.objects.annotate(
            borrow_count=Count('borrowrequest', filter=Q(borrowrequest__status__in=['accepted', 'renew_accpect']))
        ).values('id', 'Username', 'borrow_count')
    )
    renewal_requests = {r.borrow_id_id: r.request_date for r in RenewalRequests.objects.all()}
    most_borrowed = (
        BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect'])
        .values('book__id', 'book__title', 'book__author')
        .annotate(borrow_count=Count('id'))
        .order_by('-borrow_count')
        .first()
    )
  
    context = {
        'borrowed_books': borrowed_books,
        'renewal_requests': renewal_requests,
        'most_borrowed': most_borrowed,
        'user_borrow_stats': user_borrow_stats, 
        'today':today,
        'accepted_statuses': ['accepted', 'renewal_accepted'],
        'admin_date':admin_data
    }
    html_content=render_to_string('admin/borrowed_books_report.html', context)
    return HttpResponse(html_content)

def download_borrowed_books_report(request):
    """
    Download the borrowed books report in PDF format.

    Args:
        request (HttpRequest): The incoming request from the client.

    Returns:
        HttpResponse: PDF file of the borrowed books report.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="borrowed_books_report.pdf"'

    CUSTOM_HEIGHT = 1000
    CUSTOM_WIDTH = 1200
    CUSTOM_SIZE = (CUSTOM_WIDTH, CUSTOM_HEIGHT)
    p = canvas.Canvas(response, pagesize=CUSTOM_SIZE)
    width, height = CUSTOM_SIZE

    p.setFont("Helvetica-Bold", 18)
    p.drawString(400, height - 50, "Borrowed Books Report")

    generated_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    p.setFont("Helvetica", 14)
    p.drawString(400, height - 70, f"Generated on: {generated_time}")

    borrowed_books = BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect', 'renewal_requested'])
    total_borrowed_books = borrowed_books.count()

    most_borrowed = (
        BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect'])
        .values('book__id', 'book__title', 'book__author')
        .annotate(borrow_count=Count('id'))
        .order_by('-borrow_count')
        .first()
    )

    if most_borrowed:
        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 100, f"Total Borrowed Books: {total_borrowed_books}")
        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 130, "Most Borrowed Book:")
        p.setFont('Helvetica', 14)
        p.drawString(50, height - 160, f"Title: {most_borrowed['book__title']}")
        p.drawString(50, height - 190, f"Author: {most_borrowed['book__author']}")
        p.drawString(50, height - 220, f"Times Borrowed: {most_borrowed['borrow_count']}")

    data = [
        ['ID', 'User', 'Email', 'Book', 'Issued Date', 'Due Date', 'Status', 'Renewal', 'Approval']
    ]

    for index,req in enumerate(borrowed_books):
        data.append([
            index + 1, req.user.Username, req.user.email, req.book.title,
            req.IssuedDate.strftime('%Y-%m-%d') if req.IssuedDate else 'N/A',
            req.Duedate.strftime('%Y-%m-%d') if req.Duedate else 'N/A',
            req.status,
            'Yes' if req.status in ['renewal_requested', 'renew_accpect'] else 'No',
            'Approved' if req.status == 'renew_accpect' else 'Rejected' if req.status == 'renew_reject' else 'Pending' if req.status == 'renewal_requested' else 'N/A'
        ])
    custom_table_color = colors.HexColor("#417690")
    table = Table(data, colWidths=[50, 100, 150, 250, 100, 100, 100, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_table_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 280, "Borrowed Books")

    table.wrapOn(p, width - 100, height - 300)
    table.drawOn(p, 50, height - 520)

    user_borrow_stats = (
        UserInfo.objects.annotate(
            borrow_count=Count('borrowrequest', filter=Q(borrowrequest__status__in=['accepted', 'renew_accpect']))
        ).values('id', 'Username', 'borrow_count')
    )

    data1 = [['User ID', 'Username', 'Books Borrowed']]
    for user in user_borrow_stats:
        data1.append([user['id'], user['Username'], user['borrow_count']])

    table1 = Table(data1, colWidths=[100, 150, 150])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_table_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    p.showPage()    
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, "User Borrow Statistics")
    table1.wrapOn(p, width - 50, height - 700)
    table1.drawOn(p, 50, height - 600)

    p.save()
    return response


def overdue_books_report(request):
    """
    Generate a report of overdue books (due date past current date).

    Args:
        request (HttpRequest): The incoming request from the client.

    Returns:
        HttpResponse: Rendered HTML page for overdue books.
    """
    today = datetime.now().date()
    overdue_books = BorrowRequest.objects.filter(status__in=['accepted','renew_accpect','renewal_requested'],Duedate__lt=now().date())
    for book in overdue_books:
        book.overdue_days = (today - book.Duedate).days
    total_overdue_books = overdue_books.count()
    context = {
        'overdue_books': overdue_books,
        'total_overdue_books': total_overdue_books
    }
    html_content=render_to_string('admin/overdue_books_report.html', context)
    return HttpResponse(html_content)


def download_overdue_books_report(request):
    """
    Download the overdue books report in PDF format.

    Args:
        request (HttpRequest): The incoming request from the client.

    Returns:
        HttpResponse: PDF file of the overdue books report.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="overdue_books_report.pdf"'

    CUSTOM_WIDTH=2500
    CUSTOM_HEIGHT=1500
    CUSTOM_SIZE=(CUSTOM_WIDTH,CUSTOM_HEIGHT)
    p = canvas.Canvas(response, pagesize=CUSTOM_SIZE)
    width, height = CUSTOM_SIZE

    p.setFont("Helvetica-Bold", 50)
    p.drawString(1000, height - 50, "Overdue Books Report")

    generated_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    p.setFont("Helvetica", 36)
    p.drawString(1000, height - 100, f"Generated on: {generated_time}")

    # Get overdue books (due date before today and not returned)
    overdue_books = BorrowRequest.objects.filter(status__in=['accepted','renew_accpect','renewal_requested'],Duedate__lt=now().date())

  
    total_overdue_books = overdue_books.count()
    p.setFont("Helvetica",36)
    p.drawString(80, height - 150, f"Total Overdue Books: {total_overdue_books}")
    print('total_overdue_books:',total_overdue_books)

    data = [['Member ID','Borrowed By','Email','Contact No','Book ID','Title','Author', 'Issued Date', 'Due Date','Status','Overdue Days']]
    for index,req in enumerate(overdue_books):
        overdue_days=(datetime.now().date() - req.Duedate).days
        data.append([index+1,req.user.Username,req.user.email,req.user.phone,index+1,req.book.title,req.book.author, str(req.IssuedDate), str(req.Duedate),req.status,overdue_days])
        print(f"Overdue Days Calculation: {(datetime.now().date() - req.Duedate).days}")
    print("Table Data:")
    for row in data:
        print(row)    
   
    custom_table_color = colors.HexColor("#417690")
    table = Table(data, colWidths=[200,200, 350, 200, 200,250,200,200,200,200,200],rowHeights=[60]*2)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_table_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE',(0,0),(-1,-1),24),
        ('ROWSIZE',(0,0),(-1,-1),50)
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 80, height - 400)

    p.showPage()
    p.save()
    return response


def member_activities_report(request):
    """
    View to generate the member activities summary for the admin panel.

    This function collects and aggregates data related to borrow requests, notifications,
    login/logout times, and renewal statuses for each user. It prepares context data for
    rendering the member activity HTML report.

    Returns:
        HttpResponse: Rendered HTML content of the member activities report.
    """
    users = UserInfo.objects.all()

    user_data = []
    total_return_count = 0
    total_cancel_count = 0
    total_pending_count = 0
    total_rejected_count = 0
    total_accepted_count = 0
    total_renewal_request_count = 0
    total_renewal_rejected_count=0
    total_renewal_accepted_count=0
    
    for user in users:
        borrow_count = BorrowRequest.objects.filter(user=user).count()
        return_count = BorrowRequest.objects.filter(user=user,status='book_returned').count()
        cancel_count = BorrowRequest.objects.filter(user=user,status='Cancel_Request').count()
        pending_count = BorrowRequest.objects.filter(user=user,status='pending').count()
        rejected_count = BorrowRequest.objects.filter(user=user,status='rejected').count()
        accepted_count = BorrowRequest.objects.filter(user=user,status='accepted').count()
        renewal_request_count = BorrowRequest.objects.filter(user=user,status='renewal_requested').count()
        renewal_rejected_count=BorrowRequest.objects.filter(user=user,status='renew_accpect').count()
        renewal_accepted_count=BorrowRequest.objects.filter(user=user,status='renew_reject').count()
        notification_count = Notification.objects.filter(user=user).count()
        last_login = user.login_time if user.login_time else "N/A"
        last_logout = user.logout_time if user.logout_time else "N/A"
        
       
        user_data.append({
            'user': user,
            'borrow_count': borrow_count,
            'notification_count': notification_count,
            'last_login': last_login,
            'last_logout': last_logout
        })
        


        total_return_count += return_count
        total_cancel_count += cancel_count
        total_pending_count += pending_count
        total_rejected_count += rejected_count
        total_accepted_count += accepted_count
        total_renewal_request_count += renewal_request_count
        total_renewal_rejected_count+= renewal_rejected_count
        total_renewal_accepted_count+= renewal_accepted_count

    member_activities = MemberActivity.objects.select_related('user', 'book').all()
 
    # print("last activity: ",last_activity) 
    context = {
        'users': users,
        'user_data': user_data,
        'borrow_requests': BorrowRequest.objects.all(),
        'member_activities': member_activities,
        'return_count': total_return_count,  
        'cancel_count': total_cancel_count,
        'pending_count': total_pending_count,
        'rejected_count': total_rejected_count,
        'accepted_count': total_accepted_count,
        'renewal_request_count': total_renewal_request_count,
        'renewal_rejected_count': total_renewal_rejected_count,
        'renewal_accepted_count': total_renewal_accepted_count,
    }
    html_content=render_to_string('admin/member_activities_report.html', context)
    return HttpResponse(html_content)

def download_member_activities_report(request):
    """
    View to generate and download a detailed member activities report as a PDF.

    This function creates a landscape A3-sized PDF that includes:
    - Basic user information
    - Borrow request and notification summary
    - Detailed borrow activity records
    - Member activity logs including request, return, renewal, login/logout dates

    Returns:
        HttpResponse: PDF file response containing the member activities report.
    """
    ...
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="member_activities_report.pdf"'

    # Set larger page size for better table fit
    p = canvas.Canvas(response, pagesize=landscape(A3))
    width, height = landscape(A3)

    # Title
    p.setFont("Helvetica-Bold", 20)
    p.drawString(width / 2 - 100, height - 50, "Member Activities Report")

    generated_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    p.setFont("Helvetica", 14)
    p.drawString(width / 2 - 100, height - 80, f"Generated on: {generated_time}")

    p.setFont("Helvetica-Bold", 20)
    p.drawString(80, height - 120, "User Details")

    # First table: User basic details
    users = UserInfo.objects.all()
    user_data = [['Username', 'Email', 'Firstname', 'Lastname', 'Phone Number', 'Date of registration']]

    for user in users:
        user_data.append([
            user.Username, user.email, user.firstname, user.lastname, user.phone, user.created_at.strftime('%Y-%m-%d')
        ])

    table = Table(user_data, colWidths=[100, 250, 100, 100, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#417690")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(p, width - 50, height - 400)
    table.drawOn(p, 80, height - 680)

    # Start a new page before the next table
    p.showPage()
    p.setFont("Helvetica-Bold", 20)
    p.drawString(80, height - 50, "Borrow and Notification Summary")

    # Second table: Borrow Requests and Notifications
    data = [['Username', 'Email', 'Borrow Requests', 'Notifications']]
    for user in users:
        borrow_count = BorrowRequest.objects.filter(user=user).count()
        notification_count = Notification.objects.filter(user=user).count()
        data.append([user.Username, user.email, borrow_count, notification_count])

    table1 = Table(data, colWidths=[150, 300, 150, 150])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#417690")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table1.wrapOn(p, width - 50, height - 400)
    table1.drawOn(p, 80, height - 600)

    activity_data = [['Borrowed By', 'Title', 'Status', 'Issued Date', 'Due Date']]
    borrow_requests = BorrowRequest.objects.all()

    for request_obj in borrow_requests:
        activity_data.append([
            request_obj.user.Username,
            request_obj.book.title,
            request_obj.get_status_display(),
            request_obj.IssuedDate.strftime('%Y-%m-%d') if request_obj.IssuedDate else 'N/A',
            request_obj.Duedate.strftime('%Y-%m-%d')
        ])

    table2 = Table(activity_data, colWidths=[100, 200, 100, 90, 90])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#417690")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Start another page before drawing the third table
    p.showPage()
    p.setFont("Helvetica-Bold", 16)
    p.drawString(80, height - 50, "Detailed Borrow Activity")
    # p.drawString(f'Total Returned Books: {}')

 
    table2.wrapOn(p, width - 50, height - 400)
    table2.drawOn(p, 80, height - 780)

    p.showPage()
    p.setFont("Helvetica-Bold", 20)
    p.drawString(80, height - 50, "Member Activity")

    # Define styles for better text wrapping
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]

    # Table 4: Member Activities
    review_data = [['Username', 'Status', 'Book Request Date', 'Accept/Reject Date', 
                    'Renewal Requested Accept/Reject Date', 'Return Date', 'Cancel Date', 
                    'Issued Date', 'Last Login', 'Last Logout']]

    activities = MemberActivity.objects.select_related('user', 'book').all()

    for activity in activities:
        review_data.append([
            Paragraph(activity.user.Username, styleN),
            Paragraph(activity.get_status_display(), styleN),
            Paragraph(activity.request_date.strftime('%Y-%m-%d') if activity.request_date else 'N/A', styleN),
            Paragraph(activity.accept_reject_date.strftime('%Y-%m-%d') if activity.accept_reject_date else 'N/A', styleN),
            Paragraph(activity.renewal_accept_reject_date.strftime('%Y-%m-%d') if activity.renewal_accept_reject_date else 'N/A', styleN),
            Paragraph(activity.return_date.strftime('%Y-%m-%d') if activity.return_date else 'N/A', styleN),
            Paragraph(activity.cancel_date.strftime('%Y-%m-%d') if activity.cancel_date else 'N/A', styleN),
            Paragraph(activity.issued_date.strftime('%Y-%m-%d') if activity.issued_date else 'N/A', styleN),
            Paragraph(activity.login_time.strftime('%Y-%m-%d %H:%M') if activity.login_time else 'N/A', styleN),
            Paragraph(activity.logout_time.strftime('%Y-%m-%d %H:%M') if activity.logout_time else 'N/A', styleN),
        ])

    # Dynamically calculate column widths to fit within the page
    num_cols = len(review_data[0])
    available_width = width - 100  # Leave margins on both sides
    col_widths = [max(80, available_width / num_cols) for _ in range(num_cols)]

    table3 = Table(review_data, colWidths=col_widths)

    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#417690")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Ensure the table fits on the page
    table3.wrapOn(p, width - 50, height - 400)
    table3.drawOn(p, 80, height - 1100)
    
    doc = SimpleDocTemplate(response, pagesize=landscape(A3))
    elements = []

    # Add the table to elements list
    elements.append(table3)

    # Build the PDF document
    doc.build(elements)

    p.save()
    return response

@csrf_exempt
def custom_admin_login(request):
    storage = get_messages(request)
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_staff:  # Only allow staff/admin users
                    login(request, user)
                    print('go to dashboard')
                    return redirect('custom_admin_dashboard')
                else:
                    messages.error(request, "You are not authorized to access this page.")
            else:
                messages.error(request, "Invalid username or password.")

    login_page_html = render_to_string('admin/login.html', {
        'form': form,
        'site_header': 'Admin Site',
      })
    return HttpResponse(login_page_html)


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_logout(request):
    """
    Logs out an authenticated admin (staff) user by clearing the session 
    and deleting authentication-related cookies.

    This view is restricted to users who are both logged in and marked as staff.
    After logout, the user is redirected to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A response redirecting the user to the login page.
    """
    request.session.flush()
    response = redirect(reverse('login'))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def custom_admin_dashboard(request):
    """
    Displays the admin dashboard with statistics and records related to users, books, 
    and borrow requests. Supports optional filtering by date range for issued books 
    and borrow statuses.

    Authenticates the staff user, fetches all users, books, and borrow request data, 
    calculates various statistics including total issued, pending, returned, and 
    overdue books. If a date range is provided in the POST request, the statistics 
    are filtered accordingly.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of the admin dashboard with statistical context.
    """
    print("admin dashboard method is called")
    users = UserInfo.objects.all()
    books = Book.objects.all()
    borrow_requests = BorrowRequest.objects.select_related('user', 'book').all()
    recent_notifications = Notification.objects.order_by('-timestamp')
    total_issued_books = BorrowRequest.objects.filter(status__in =['accepted','renew_accpect']).count()
    total_pending_borrow_requests = BorrowRequest.objects.filter(status='pending').count()
    total_pending_renewal_requests = BorrowRequest.objects.filter(status='renewal_requested').count()
    total_returned_books = BorrowRequest.objects.filter(status='book_returned').count()
    total_not_returned_books = BorrowRequest.objects.filter(status__in =['accepted','renew_accpect','renewal_requested'],Duedate__lt=now().date()).count()
    print("not",total_not_returned_books)
    total_not_returned_bookss = BorrowRequest.objects.filter(status__in =['accepted','renew_accpect','renewal_requested'],Duedate__lt=now())
    print("non returned books",total_not_returned_bookss)
    date_range= request.POST.get('date_range')
    print("this is the start and end date:",date_range)
    start_date = None
    end_date = None

    
    if date_range:
        try:
            start_str, end_str = date_range.split(" - ")
            start_date = datetime.strptime(start_str.strip(), "%m/%d/%Y").date()
            end_date = datetime.strptime(end_str.strip(), "%m/%d/%Y").date()
        except ValueError:
            print("Invalid date format received.")

    if start_date and end_date:
        filter_borrow_requests = borrow_requests.filter(IssuedDate__range=(start_date, end_date))
        filter_total_issued_books = BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect'], IssuedDate__range=(start_date, end_date)).count()
        filter_total_pending_borrow_requests = BorrowRequest.objects.filter(status='pending', IssuedDate__range=(start_date, end_date)).count()
        filter_total_pending_renewal_requests = BorrowRequest.objects.filter(status='renewal_requested', IssuedDate__range=(start_date, end_date)).count()
        filter_total_returned_books = BorrowRequest.objects.filter(status='book_returned', IssuedDate__range=(start_date, end_date)).count()
        filter_total_not_returned_books = BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect','renewal_requested'], 
        IssuedDate__range=(start_date, end_date),Duedate__lt=now().date()).count()
        
    else:
        # If no date range is selected, use total counts
        filter_borrow_requests=borrow_requests
        filter_total_issued_books = total_issued_books
        filter_total_pending_borrow_requests = total_pending_borrow_requests
        filter_total_pending_renewal_requests = total_pending_renewal_requests
        filter_total_returned_books = total_returned_books
        filter_total_not_returned_books = total_not_returned_books

    dashboard_html = render_to_string('admin/dashboard.html', {
        'users': users,
        'books': books,
        'borrow_requests': borrow_requests,
        'notifications': recent_notifications,
        'total_issued_books':total_issued_books,
        'total_not_returned_books':total_not_returned_books,
        'total_pending_borrow_requests':total_pending_borrow_requests,
        'total_pending_renewal_requests':total_pending_renewal_requests,
        'total_returned_books':total_returned_books,
        'admin_user':request.user,
        'start_date':start_date,
        'end_date':end_date,

        'filter_borrow_requests': filter_borrow_requests,
        'filter_total_issued_books':filter_total_issued_books,
        'filter_total_not_returned_books':filter_total_not_returned_books,
        'filter_total_pending_borrow_requests':filter_total_pending_borrow_requests,
        'filter_total_pending_renewal_requests':filter_total_pending_renewal_requests,
        'filter_total_returned_books':filter_total_returned_books,
    })
    return HttpResponse(dashboard_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def custom_books(request):
    """
    Displays the list of all books for the admin user.

    Authenticates the staff user, retrieves all book records from the database, 
    and renders the 'books.html' template with the list of books.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of the books page with all book records.
    """
    books = Book.objects.all()
    books_html = render_to_string('admin/books.html', {'books': books})
    return HttpResponse(books_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def custom_book_add(request):
    """
    Handles the addition of a new book by the admin.

    Authenticates the staff user, processes POST request to create a new book, triggers the BookAdmin model logic to create copies, and redirects to the book list.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the book list on successful POST, else renders the book add form.
    """
    print("Add Book Method Called")
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        description = request.POST.get('description')
        quantity = int(request.POST.get('quantity', 0))

        Book.objects.create(
            title=title,
            author=author,
            category=category,
            description=description,
            quantity=quantity
        )
        admin_instance = BookAdmin(Book, admin.site)  
        print("callind admin instance for creating copy of book in copytable ")
        admin_instance.save_model(request, Book, None, False)
        print("redirecting to manage book")
        return redirect('custom_books')

    form_html = render_to_string('admin/book_add.html')
    return HttpResponse(form_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_borrow_request(request):
    """
    Displays all pending borrow requests for the admin.

    Fetches borrow requests with 'pending' status and renders them to the template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML showing pending borrow requests.
    """
    borrow_requests=BorrowRequest.objects.filter(status__in =['pending'])
    borrow_request_html = render_to_string('admin/borrow_request.html', {
        'borrow_requests': borrow_requests,
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_pending_renewal_request(request):
    """
    Displays pending renewal requests for the admin.

    Fetches borrow requests with 'renewal_requested' status and renders them.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of pending renewal requests.
    """
    borrow_requests=BorrowRequest.objects.filter(status__in =['renewal_requested'])
    borrow_request_html = render_to_string('admin/pending_renewal.html', {
        'borrow_requests': borrow_requests,   
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_issued_book(request):
    """
    Displays currently issued books for the admin.

    Fetches borrow requests with 'accepted' or 'renew_accpect' status and renders them.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of issued books.
    """
    borrow_requests=BorrowRequest.objects.filter(status__in =['accepted','renew_accpect'])
    borrow_request_html = render_to_string('admin/issued_book.html', {
        'borrow_requests': borrow_requests, 
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_returned_book(request):
    """
    Displays books that have been returned by users.

    Fetches borrow requests with 'book_returned' status and renders them.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of returned books.
    """
    borrow_requests=BorrowRequest.objects.filter(status='book_returned')
    borrow_request_html = render_to_string('admin/returned_book.html', {
        'borrow_requests': borrow_requests,  
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_borrow_history(request):
    """
    Displays complete borrow history for all users.

    Retrieves all borrow requests and renders them for the admin to review.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of full borrow history.
    """
    borrow_requests = BorrowRequest.objects.select_related('user').all()
    borrow_request_html = render_to_string('admin/borrow_history.html', {
        'borrow_requests': borrow_requests,  
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_not_returned_book(request):
    """
    Displays the list of books not returned after the due date.

    Fetches borrow requests with due dates earlier than today and status 
    indicating the book is still with the user. Renders the overdue list.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of overdue books.
    """
    borrow_requests = BorrowRequest.objects.select_related('user').filter(status__in=['accepted','renew_accpect','renewal_requested'],Duedate__lt=now().date())
    borrow_request_html = render_to_string('admin/non_returned_book.html', {
        'borrow_requests': borrow_requests,'today': timezone.now().date()
        })  
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user(request):
    """
    Displays the list of all users for the admin.

    Fetches all user records and renders them in the admin interface.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML of user list.
    """
    users = UserInfo.objects.all()
    user_html = render_to_string('admin/user.html', {
        'users': users,
    })
    return HttpResponse(user_html)
    
@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_members(request):
    """
    Displays a list of all library members for administrative management.

    Authenticates admin user, retrieves all user records from the database,
    and renders the 'manage_members.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML displaying all members.
    """
    users = UserInfo.objects.all()
    user_html = render_to_string('admin/manage_members.html', {'users': users})
    return HttpResponse(user_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_member(request):
    """
    Handles adding a new member to the system by the admin.

    Displays a form to add a member. On POST, saves user details,
    logs the action, and redirects to member list.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders form or redirects on success.
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            member=form.save()
            AdminActions.objects.create(
                admin_id=request.user,
                action_type="Add Member",
                description=f"Added Member: {member.Username}"
            )
            messages.success(request, "Member added successfully!")
            return redirect('manage_members')
    else:
        form = UserForm()
    user_html = render_to_string('admin/add_member.html', {'form': form})
    return HttpResponse(user_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_member(request, member_id):
    """
    Allows the admin to update details of an existing member.

    Loads the member by ID, displays pre-filled form, updates on valid POST,
    logs the admin action, and redirects to members list.

    Args:
        request (HttpRequest): The HTTP request object.
        member_id (int): ID of the member to edit.

    Returns:
        HttpResponse: Rendered form or redirection to members list.
    """
    print(f"edit_member called with member_id: {member_id}")
    member = get_object_or_404(UserInfo, id=member_id)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member=form.save()
            AdminActions.objects.create(
                admin_id=request.user,
                action_type="Edit Member",
                description=f"Edited Member: {member.Username}"
            )

            return redirect('manage_members')  
    else:
        form = UserForm(instance=member)
    user_html = render_to_string('admin/edit_member.html', {'form': form})
    return HttpResponse(user_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_member(request, user_id):
    """
    Allows admin to delete a member from the system.

    Authenticates admin, deletes the user by ID, logs the action,
    and redirects to member list.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): ID of the user to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to manage_members view.
    """

    user = get_object_or_404(UserInfo, id=user_id)
    user.delete()
    AdminActions.objects.create(
                admin_id=request.user,
                action_type="Delete Member",
                description=f"Deleted Member: {user.Username}"
            )
    return redirect('manage_members')

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_books(request):
      """
    Displays the list of all books for admin to manage.

    Authenticates admin user, fetches all book records, 
    and renders the 'manage_books.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML with list of books.
    """
      print("manage books called")
      books = Book.objects.all()
      book_html = render_to_string('admin/manage_books.html', {'books':books})
      return HttpResponse(book_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    """
    Adds a new book to the library collection.

    Displays a form to add a book. On POST, saves the book, logs the action,
    and redirects to book management view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Form to add book or redirect on success.
    """
    print('inside add_book')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book=form.save()
            AdminActions.objects.create(
                admin_id=request.user,
                action_type="Add Book",
                description=f"Added book: {book.title}"
            )
            print("redirecting to custom book")
            return redirect('manage_books')
    else:
        form = BookForm()
    book_html = render_to_string('admin/add_book.html', {'form': form})
    return HttpResponse(book_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_book(request, book_id):
    """
    Allows the admin to edit details of an existing book.

    Loads book by ID, displays editable form, updates book on POST,
    logs the update, and redirects.

    Args:
        request (HttpRequest): The HTTP request object.
        book_id (int): ID of the book to be edited.

    Returns:
        HttpResponse: Rendered edit form or redirect.
    """
    print(f"edit_member called with member_id: {book_id}")
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            AdminActions.objects.create(
                admin_id=request.user,
                action_type="Edit Book",
                description=f"Edited book: {book.title}"
            )
            return redirect('manage_books')  
    else:
        form = BookForm(instance=book)
    book_html = render_to_string('admin/edit_book.html', {'form': form})
    return HttpResponse(book_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, book_id):
    """
    Deletes a book from the collection.

    Authenticates admin, deletes book by ID, logs the action,
    and redirects to manage_books.

    Args:
        request (HttpRequest): The HTTP request object.
        book_id (int): ID of the book to be deleted.

    Returns:
        HttpResponseRedirect: Redirect to book management view.
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    AdminActions.objects.create(
                admin_id=request.user,
                action_type="Delete Book",
                description=f"Deleted book: {book.title}"
            )
   
    return redirect('manage_books')

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def bulk_upload_books(request):
    """
    Uploads multiple books from an Excel file via a form.

    Renders a bulk upload form and processes file on valid POST,
    handles errors, and redirects to book management.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Bulk upload form or redirect on success.
    """
    if request.method == "POST":
        form = BookBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.process_file(request.user)
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
            return redirect('manage_books')
    else:
        form = BookBulkUploadForm()
    storage = get_messages(request)
    book_html = render_to_string('admin/bulk_upload.html', {'form': form, 'messages': storage})
    return HttpResponse(book_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_notification(request):
    """
    Displays all recent system notifications for the admin.

    Fetches notifications ordered by timestamp and renders them
    in the admin panel.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML showing notifications.
    """
    recent_notifications = Notification.objects.order_by('-timestamp')
    user_html = render_to_string('admin/notification.html', {
        'notifications': recent_notifications
       
    })
    return HttpResponse(user_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def update_borrow_request_status(request, request_id):
    """
    Allows admin to update the status of a borrow request.

    On POST, updates status and optionally sets issue date,
    creates a notification, logs the update, and redirects.

    Args:
        request (HttpRequest): The HTTP request object.
        request_id (int): ID of the borrow request to update.

    Returns:
        HttpResponse: Borrow update form or redirect on success.
    """
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        borrow_request.status = new_status
        if new_status == 'accepted':
            borrow_request.IssuedDate = timezone.now().date()
        borrow_request.save()

        Notification.objects.create(
            user=borrow_request.user,
            message=f"Your borrow request for '{borrow_request.book.title}' has been {new_status}"
        )

        AdminActions.objects.create(
            admin_id=request.user,
            action_type='Borrow Request Updated',
            description=f"Updated borrow request {borrow_request.id} status to {new_status}"
        )

        return redirect('custom_admin_dashboard')

    borrow_request_html = render_to_string('admin/borrow_request_update.html', {
        'borrow_request': borrow_request,
        'status_choices': BorrowRequest.STATUS_CHOICES
    })
    return HttpResponse(borrow_request_html)

@csrf_exempt
def register_view(request):
    """
    Handle user registration:
    - Validate form input
    - Check for duplicate email or username
    - Hash the password and generate OTP
    - Send OTP to user’s email
    - Redirect to OTP verification page
    """
    print("inside register view")
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        password=request.POST.get('password')
        phone=request.POST.get('phone_number')
        confirm_password=request.POST.get('confirm-password')

        if UserInfo.objects.filter(email=email).exists():
             html_content = render_to_string( 'register.html', {'error': 'Email is already registered.'})  
             return HttpResponse(html_content)
        if User.objects.filter(username=username).exists():
             html_content = render_to_string( 'register.html', {'error': 'Username is already registered.'})  
             return HttpResponse(html_content)
        if password != confirm_password:
             html_content = render_to_string( 'register.html', {'error': 'Password do not match.'})  
             return HttpResponse(html_content)
        if not phone.isdigit():    
            html_content = render_to_string( 'register.html', {'error': 'Phone number must conatin only digit.'})  
            return HttpResponse(html_content)
 
        hashed_password=make_password(password)
        email_otp = generate_otp() 
        print(email_otp)
        user=UserInfo.objects.create(Username=username,email=email,firstname=firstname,lastname=lastname,phone=phone,email_otp=email_otp,password=hashed_password)

        send_mail(
            'OTP Code',
            f'Your OTP for Registartion is: {email_otp}',
            settings.EMAIL_HOST_USER,
            [email]
        )
        print("redirecting to verify_otp page")
        return redirect('verify-otp', user_id=user.id)  # Redirect to OTP verification page

    else:
        pass

    html_content = render_to_string('register.html')  
    return HttpResponse(html_content)

@csrf_exempt
def verify_otp(request, user_id):
    """
    Verify the OTP entered by the user.
    - If 'resend' is clicked, send a new OTP
    - If OTP is valid, mark email as verified and redirect to home
    - Otherwise, show error
    """
    try:
        user = UserInfo.objects.get(id=user_id)
    except UserInfo.DoesNotExist:
        html_content = render_to_string('Otp.html', {
            'error': 'User not found.',
            'user_id': user_id
        })
        return HttpResponse(html_content)

    if request.method == 'POST':
        print("resend otp")
        print(request.POST)
        if 'resend' in request.POST:
            # If the resend OTP button was clicked
            new_otp = generate_otp()
            user.email_otp = new_otp
            user.save()
            print("sending mail")
            send_mail(
                'Resent OTP Code',
                f'Your new OTP for registration is: {new_otp}',
                settings.EMAIL_HOST_USER,
                [user.email]
            )

            html_content = render_to_string('Otp.html', {
                'message': 'A new OTP has been sent to your email.',
                'user_id': user_id
            })
            return HttpResponse(html_content)

        # Otherwise, handle OTP verification
        email_otp = request.POST.get('email_otp', '').strip()

        if verifyotp(email_otp, user.email_otp):
            user.is_email_verified = True
            user.save()
            return redirect('/')  # Redirect to login page
        else:
            html_content = render_to_string('Otp.html', {
                'error': 'Invalid OTP',
                'user_id': user_id
            })
            return HttpResponse(html_content)

    html_content = render_to_string('Otp.html', {'user_id': user_id})
    return HttpResponse(html_content)


@csrf_exempt
def resend_otp(request, user_id):
    """
    Resend a new OTP to the user’s email.
    """
    user = UserInfo.objects.get(id=user_id)
    new_otp = generate_otp() 
    user.email_otp = new_otp  
    user.save()

    send_mail(
        'OTP Code - Resend',
        f'Your new OTP is: {new_otp}',
        settings.EMAIL_HOST_USER,
        [user.email]
    )

    html_content = render_to_string('Otp.html', {'message': 'OTP resent successfully! Check your email.', 'user_id': user_id})  
    return HttpResponse(html_content)

@csrf_exempt
def login_view(request):
        """
        Handle login for:
        - Admin users (using Django's User model)
        - Regular users (using custom UserInfo model)
        On success: generate and set access and refresh tokens
       """
        if request.method == 'POST':
            identifier = request.POST.get('identifier')  # Accepts email or username
            password = request.POST.get('password')

            # **Check if user is in Django's built-in User model (Admin Login)**
            admin_user = authenticate(request, username=identifier, password=password)
            if admin_user:
                if admin_user.is_staff:  # Allow only staff/admin users
                    login(request, admin_user)
                    return redirect('custom_admin_dashboard')  # Redirect to Django Admin panel
                else:
                    html_content = render_to_string('login.html', {'error': 'Access denied for non-admin users.'})
                    return HttpResponse(html_content)

            # **Check if user is in UserInfo model**
            try:
                user_info = UserInfo.objects.get(email=identifier)  # Check if it's an email
            except UserInfo.DoesNotExist:
                try:
                    user_info = UserInfo.objects.get(Username=identifier)  # Check if it's a username
                except UserInfo.DoesNotExist:
                    html_content = render_to_string('login.html', {'error': 'User does not exist'})
                    return HttpResponse(html_content)

            # **Verify password**
            if check_password(password, user_info.password):
                access_token_payload = {
                    'email': user_info.email,
                    'exp': datetime.now() + settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'],
                    'iat': int(time.time()),
                }
                access_token = jwt.encode(access_token_payload, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithm=settings.JWT_AUTH['JWT_ALGORITHM'])

                refresh_token_payload = {
                    'email': user_info.email,
                    'exp': datetime.now() + settings.JWT_AUTH['JWT_REFRESH_TOKEN_LIFETIME'],
                    'iat': int(time.time()),
                }
                refresh_token = jwt.encode(refresh_token_payload, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithm=settings.JWT_AUTH['JWT_ALGORITHM'])

                RefreshTokenStore.objects.filter(user=user_info).delete()
                RefreshTokenStore.objects.create(user=user_info, token=refresh_token,access_token=access_token)
                
                user_info.login_time = now()
                user_info.save(update_fields=['login_time'])

              
                response = redirect('home')
                response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax',max_age=settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'].total_seconds(),)
                response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Lax',max_age=settings.JWT_AUTH['JWT_REFRESH_TOKEN_LIFETIME'].total_seconds())
                return response
            else:

                html_content = render_to_string('login.html', {'error': 'Invalid credentials'})
                return HttpResponse(html_content)

        html_content = render_to_string('login.html')
        return HttpResponse(html_content)

def refresh_token_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    
    if not refresh_token:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')

    try:
        payload = jwt.decode(
            refresh_token, 
            settings.JWT_AUTH['JWT_SECRET_KEY'], 
            algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']]
        )
        user = UserInfo.objects.get(email=payload['email'])

        # Check if refresh token is stored
        refresh_token_obj = RefreshTokenStore.objects.filter(user=user, token=refresh_token).first()
        if not refresh_token_obj:
            messages.error(request, "Session expired. Please log in again.")
            return redirect('login')

        # Generate new access token
        access_token_payload = {
            'email': user.email,
            'exp': datetime.now() + settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'],
           'iat': int(time.time()),
        }
        access_token = jwt.encode(
            access_token_payload, 
            settings.JWT_AUTH['JWT_SECRET_KEY'], 
            algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
        )

        # Set new access token in cookies
        response = redirect('home')
        response.set_cookie(
            'access_token', access_token, httponly=True, secure=True, samesite='Lax',
            max_age=settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'].total_seconds()
        )
        return response

    except jwt.ExpiredSignatureError:
        #  If the refresh token is expired, force logout
        messages.error(request, "Session expired. Please log in again.")
        response = redirect('login')
        response.delete_cookie('access_token')  # Clear old access token
        response.delete_cookie('refresh_token')  # Clear expired refresh token
        return response

    except (jwt.DecodeError, UserInfo.DoesNotExist):
        messages.error(request, "Invalid session. Please log in again.")
        return redirect('login')

@csrf_exempt
def email(request):
    """
    Handles email input for OTP-based password reset.

    - If method is POST:
        - Checks if email exists in the database.
        - Generates and sends OTP to the email if exists.
        - Redirects to OTP verification page.
    - If method is GET:
        - Renders the email input form.
    """

    if request.method == 'POST':
        email = request.POST.get('email')

        if UserInfo.objects.filter(email=email).exists():
            user = UserInfo.objects.get(email=email)  
            email_otp = generate_otp()

          
            user.email_otp = email_otp
            user.save()

            send_mail(
                'OTP For Reset Password',
                f'Your OTP code is: {email_otp}',
                settings.EMAIL_HOST_USER,
                [email]
            )
            return redirect('otp', user_id=user.id)  
        else:
            html_content = render_to_string('email.html',{'error': 'Email does not exist. Register first.'})  
            return HttpResponse(html_content)

    html_content = render_to_string('email.html')  
    return HttpResponse(html_content)

@csrf_exempt
def otp_password(request, user_id):
    """
    Verifies the OTP for the given user and redirects to reset password page if correct.

    - Retrieves user by ID.
    - If method is POST:
        - Compares entered OTP with the one stored.
        - Redirects to password reset page on success.
        - Otherwise, shows error.
    - If method is GET:
        - Renders the OTP entry form.
    """
    try:
        # Get user by user_id, NOT by JWTAuthentication
        user = UserInfo.objects.get(id=user_id)
    except UserInfo.DoesNotExist:
        return HttpResponse("User not found", status=404)
    
    if request.method == 'POST':
        email_otp = request.POST.get('email_otp','').strip()  

        if verifyotp(email_otp, user.email_otp): 
            return redirect('reset_password', user_id=user.id)  
        else:
            html_content = render_to_string('otp.html',{'error': 'Invalid OTP', 'user_id': user_id})  
            return HttpResponse(html_content)
         
    html_content = render_to_string('otp.html',{'user_id': user_id})  
    return HttpResponse(html_content)
   

@csrf_exempt
def reset_password(request, user_id):
    """
    Allows user to reset their password after OTP verification.

    - If POST:
        - Validates password strength and match.
        - Hashes and saves new password.
        - Redirects to login/homepage on success.
    - If GET:
        - Renders the reset password form.
    """
    user = UserInfo.objects.get(id=user_id) 
    if request.method == 'POST':
        password = request.POST.get('password') 
        confirm_password = request.POST.get('check-password')  
        try:
            validate_password(password)  # Check password strength
        except ValidationError as e:
            html_content = render_to_string('reset_password.html', {'error': e.messages, 'user_id': user_id})  
            return HttpResponse(html_content)

        if password == confirm_password:  
            user.password = make_password(password)  
            user.save()  
            return redirect('/')  
        else:
            html_content = render_to_string('reset_password.html', {'error': 'Passwords do not match or must be new.', 'user_id': user_id})  
            return HttpResponse(html_content)

    html_content = render_to_string('reset_password.html', {'user_id': user_id})  
    return HttpResponse(html_content)

# @session_login_required
def view_profile(request):
    """
    Displays the user's profile page using JWT authentication.
    
    - Redirects to login if authentication fails.
    - Renders user data on profile view.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    context = user_context_processor(request)
    html_content = render_to_string('view_profile.html', { **context,'user': user})  
    return HttpResponse(html_content)


@csrf_exempt
# @session_login_required
def edit_profile(request):
    """
    Allows the user to edit their profile details including uploading/removing a profile picture.

    - Requires JWT-based user authentication.
    - If POST:
        - Updates user details and profile picture.
        - Validates form and saves changes.
        - Redirects to same page after update.
    - If GET:
        - Displays form with current user data.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    print("User in edit_profile:", user.email)
    context = user_context_processor(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        phone = request.POST.get('phone_number')
        print("POST data:", request.POST)
        remove_picture = request.POST.get('remove_picture')
        print("Remove Picture Value:", remove_picture) 

        # Update basic fields
        user.Username = username
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone

        # Handle form for file upload
        form = ProfileForm(request.POST, request.FILES, instance=user)

        # Remove photo if user clicked "Remove Photo"
        if remove_picture == "true" :
            print("Removing profile picture...")
            if user.profile_picture:
                # Delete the file from storage
                photo_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
                if os.path.isfile(photo_path):
                    os.remove(photo_path)
                user.profile_picture.delete(save=False)
                user.profile_picture = None
            user.profile_picture = None
            user.save()     
                
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

       
        user.save() 

        if form.is_valid():
            form.save()

        return redirect('edit_profile')  # Redirect to the same page after update

    else:
        form = ProfileForm(instance=user)
        
    html_content = render_to_string('Edit_Profile.html', {**context,'form': form, 'user': user})  
    return HttpResponse(html_content)


# @session_login_required
@csrf_exempt
def home(request):
    """
    Displays the user's dashboard with a summary of borrowing activities.

    Authenticates the user and shows counts of borrowed, overdue, 
    renewal requested, returned, and pending books. Also includes unread notifications.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'home.html' dashboard page.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('/')
    user, _ = user_data
   
    context = user_context_processor(request)
    borrowed_count = BorrowRequest.objects.filter(user=user, status__in=['accepted','renew_accpect']).count()
    overdue_count = BorrowRequest.objects.filter(user=user, Duedate__lt=timezone.now(), status='accepted').count()
    renewal_count = BorrowRequest.objects.filter(user=user, status='renewal_requested').count()
    returned_count = BorrowRequest.objects.filter(user=user, status='book_returned').count()
    pending_count = BorrowRequest.objects.filter(user=user, status='pending').count()
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    

    html_content = render_to_string('home.html',{**context,'user':user,'borrowed_count': borrowed_count,
            'overdue_count': overdue_count,
            'renewal_count': renewal_count,
            'pending_count':pending_count,
            'returned_count': returned_count,
            'notification_count': 
            notification_count})  
    return HttpResponse(html_content)
  

# @session_login_required
def book_list(request):
    """
    Displays the list of all available books.

    Authenticates the user, fetches all books from the database,
    and renders the 'book.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page showing all books.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    books = Book.objects.all()  # Fetch all books from the database
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('book.html', {**context,'books': books})  
    return HttpResponse(html_content)

# @session_login_required
def book_detail(request, book_id):
    """
    Displays detailed information about a selected book.

    Authenticates the user and fetches book details like title, 
    author, and description based on the given book ID.

    Args:
        request (HttpRequest): The HTTP request object.
        book_id (int): ID of the selected book.

    Returns:
        HttpResponse: Rendered 'book_detail.html' page with book information.
    """
    user_data = JWTAuthentication().authenticate(request)
    user,_=user_data
    print("data",user_data)
    if not user_data:
        return redirect('login')
    book = get_object_or_404(Book, id=book_id)
    
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count}) 
    html_content = render_to_string('book_detail.html', {**context,'book': book})  
    return HttpResponse(html_content)

# @session_login_required
def search_books(request):
    """
    Searches books based on a query string provided by the user.

    Authenticates the user and looks up books by title, author,
    or category (case-insensitive). Returns the search results 
    rendered in the 'search_results.html' page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page showing the list of matched books.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    user,_=user_data
    if not user_data:
        return redirect('login')
    query = request.GET.get('q', '').strip()  # get search query from URL params
    books = []

    if query:
        books = Book.objects.filter(
            # check the searched content is title or author or category with Q that ingnore the case sensitive error
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)  # Add more fields as necessary
        )

    user_id = request.session.get('user_id')
    profile_user = None
    if user_id:
        profile_user = UserInfo.objects.get(id=user_id)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('search_results.html', {**context,
        'books': books,
        'query': query,
        'profile_user': profile_user})  
    return HttpResponse(html_content)

# @session_login_required
def borrow_history(request):
    """
    Displays the borrowing history of the logged-in user in descending order.

    Authenticates the user, fetches all borrow requests made by the user,
    and renders them in the 'borrow_history.html' page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page with the user's borrowing history.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    print(request.user)
    print(request.session.get('user_id'))
    
    user,_=user_data
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})

    borrow_requests = BorrowRequest.objects.filter(user=user).order_by('-id')
    # print(borrow_requests)
    html_content = render_to_string( 'borrow_history.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)


# @session_login_required
def user_book(request):
    """
    Retrieves the list of books currently borrowed by the authenticated user.

    Filters borrow requests from the BorrowRequest table where the status is either 
    'accepted' or 'renew_accpect', indicating that the user has successfully borrowed 
    or renewed the book. This helps in showing all books currently in possession of the user.

    Returns:
        HttpResponse: Rendered HTML page displaying the borrowed books.
    """

    user_data = JWTAuthentication().authenticate(request)
    user,_=user_data
    print("data",user_data)
    if not user:
        return redirect('login')
   
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
  
    context.update({'notification_count': notification_count})
   
    borrow_requests = BorrowRequest.objects.filter(user=user,status__in=['accepted','renew_accpect'])
    html_content = render_to_string('user_book.html', {**context,'borrow_requests': borrow_requests})  
    return HttpResponse(html_content)

# @session_login_required
def user_duebook(request):
    """
    Retrieves and displays a list of books that are overdue for the currently authenticated user.

    This view authenticates the user using JWT, checks for borrow requests where the status is 
    either 'accepted' or 'renew_accpect', and the due date is earlier than today. It then renders 
    the 'user_duebook.html' template with the list of overdue books and the user's unread notification count.

    Returns:
        HttpResponse: Rendered HTML page displaying the user's overdue books and notification count.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    print(user)
    today= timezone.now().date()
    borrow_requests = BorrowRequest.objects.filter(user=user,status__in=['accepted','renew_accpect'],Duedate__lt=today)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})

    html_content = render_to_string('user_duebook.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)

# @session_login_required
def pending_renewal(request):
    """
    Displays the list of books for which the user has requested a renewal 
    but the request is still pending and the due date is past.

    Authenticates the user, fetches the user's renewal requests with status 
    'renewal_requested' and a due date less than today, and renders the 
    'pending_renewals.html' template with context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page with pending renewal requests.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    today = timezone.now().date()
    borrow_requests = BorrowRequest.objects.filter(user=user,status='renewal_requested',Duedate__lt=today)
   
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('pending_renewals.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)

def pending_request(request):
    """
    Displays the list of books that the user has requested but are still 
    pending approval.

    Authenticates the user, fetches borrow requests with status 'pending',
    and renders the 'pending_request.html' template with context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page with pending book requests.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    borrow_requests = BorrowRequest.objects.filter(user=user,status='pending')
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('pending_request.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)

# @session_login_required
def returned_book(request):
    """
    Displays the list of books returned by the user where the due date 
    is greater than today.

    Authenticates the user, filters borrow requests with status 
    'book_returned' and a future due date, and renders the 
    'return_books.html' template with context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page with returned books.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    today= timezone.now().date()
    user,_ =user_data
    borrow_requests = BorrowRequest.objects.filter(user=user,status='book_returned',Duedate__gt=today)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('return_books.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)

# @session_login_required
@csrf_exempt
def request_book(request, book_id):
        """
        Handles the submission of a book request by the user.

        Authenticates the user, checks the availability of the selected book,
        creates a borrow request and logs the activity if the book is available.

        Args:
            request (HttpRequest): The HTTP request object.
            book_id (int): ID of the book to request.

        Returns:
            HttpResponseRedirect: Redirects to 'borrow_history' after processing the request.
        """
        user_data = JWTAuthentication().authenticate(request)
        print("data",user_data)
        if not user_data:
            return redirect('login')
        if request.method == "POST":
            user,_=user_data
            book = get_object_or_404(Book, id=book_id)

            if not book.is_available:
                messages.error(request, "This book is not available right now.")
                return redirect('book')

            borrow_request = BorrowRequest.objects.create(
                user=user,
                book=book,
                status="pending"
            )
            MemberActivity.objects.create(
            user=user,
            book=book,
            request_date=timezone.now(),
            status="requested"
            )
            messages.success(request, "Your request has been submitted.")
            for message in messages.get_messages(request):
                print("Message:", message)
        return HttpResponseRedirect(reverse('borrow_history'))

# @session_login_required
@csrf_exempt
def returned_books(request):
    """
    Displays the list of books that the user has returned.

    This view authenticates the user, retrieves all BorrowRequest entries with the status 
    'book_returned', calculates the current notification count, and renders the 
    'returned_books.html' template with relevant context including today's date.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page showing the list of returned books.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data

    borrow_requests = BorrowRequest.objects.filter(user=user, status='book_returned')
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('returned_books.html', {**context,
        'borrow_requests': borrow_requests,
        'today': timezone.now().date()})
    return HttpResponse(html_content)
   

# @session_login_required
@csrf_exempt
def canceled_books(request):
    """
    Displays the list of books for which the user has canceled their borrow request.

    This view authenticates the user, retrieves all BorrowRequest entries with the status 
    'Cancel_Request' (indicating cancellation), fetches unread notification count, and 
    renders the 'canceled_books.html' template with the relevant context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page showing the list of canceled borrow requests.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data

    borrow_requests = BorrowRequest.objects.filter(user=user, status='Cancel_Request')

    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('canceled_books.html', {**context,
        'borrow_requests': borrow_requests,
        'today': timezone.now().date()
    })  
    return HttpResponse(html_content)

# @session_login_required
@csrf_exempt
def renewal_books(request):
    """
    Displays the list of books for which the user has requested and received renewal approval.

    This view authenticates the user, fetches all BorrowRequest entries with status 
    'renew_accpect' (indicating approved renewals), gathers notification count, 
    and renders the 'renewal_books.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page displaying the list of renewed books.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    borrow_requests = BorrowRequest.objects.filter(user=user, status='renew_accpect')
    print(borrow_requests)
    html_content = render_to_string( 'renewal_books.html', {**context,
        'borrow_requests': borrow_requests,
        'today': timezone.now().date()
    })  
    return HttpResponse(html_content)

# @session_login_required
@csrf_exempt
def request_renewal(request,request_id):
    """
    Handles a renewal request for a borrowed book.

    This view is triggered when a user clicks the 'Renewal Request' button.
    It updates the status of the corresponding BorrowRequest to 'renewal_requested',
    creates a RenewalRequests entry, logs the activity in MemberActivity,
    and sends a WebSocket notification to the user.

    Args:
        request (HttpRequest): The HTTP request object.
        request_id (int): The ID of the BorrowRequest for which the renewal is requested.

    Returns:
        HttpResponseRedirect: Redirects the user to the borrow history page.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    borrow_request = BorrowRequest.objects.get(id=request_id)
    borrow_request.status = 'renewal_requested'
    borrow_request.save()
    
    RenewalRequests.objects.create(
        borrow_id=borrow_request,
        request_date=timezone.now()
    )
    MemberActivity.objects.create(
        user=borrow_request.user,
        book=borrow_request.book,
        renewal_request_date=timezone.now(),
        status='renewal_requested'
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{borrow_request.user.id}",
        {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
    )
    return redirect('borrow_history')   

# @session_login_required
@csrf_exempt
def cancel_book(request,request_id):
     """
    Handles the cancellation of a borrow request.

    This view is triggered when a user chooses to cancel a borrow request.
    It updates the status of the BorrowRequest to 'Cancel_Request',
    logs the cancellation in MemberActivity, sends a WebSocket notification,
    creates a user notification entry, and sends an email alert to the user.

    Args:
        request (HttpRequest): The HTTP request object.
        request_id (int): The ID of the BorrowRequest to be canceled.

    Returns:
        HttpResponseRedirect: Redirects the user to the notifications page.
     """

     user_data = JWTAuthentication().authenticate(request)
     print("data",user_data)
     if not user_data:
        return redirect('login')
     print(f"Cancelling request {request_id}") 
     cancel_request=BorrowRequest.objects.get(id=request_id)
     cancel_request.status='Cancel_Request'
     cancel_request.save()
     MemberActivity.objects.create(
        user=cancel_request.user,
        book=cancel_request.book,
        cancel_date=timezone.now(),
        status='canceled'
    )
     channel_layer=get_channel_layer()
     async_to_sync(channel_layer.group_send)(
          f"user_{cancel_request.user.id}",
         {"type":"cancel_request","status":cancel_request.status, "book":cancel_request.book.title}
     )
     Notification.objects.create(
        user=cancel_request.user,
        message=f"Your borrow request for '{cancel_request.book.title}' has been canceled.",
        is_read=False
     )

     subject = "Library Borrow Request Canceled"
     message = f"Your borrow request for '{cancel_request.book. title}' has been canceled."
     recipient_email = cancel_request.user.email  
        
     send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

        # Display message on the screen
     messages.success(request, f"Borrow request for '{cancel_request.book.title}' has been canceled successfully.")

     return redirect('notification')

# @session_login_required
@csrf_exempt
def return_book(request,request_id):
    """
    Handles the return process of a borrowed book.

    This view is triggered when a user confirms the return of a borrowed book.
    It updates the status of the BorrowRequest to 'book_returned',
    increments the book's quantity and sets its availability to True,
    logs the return activity in MemberActivity, sends a WebSocket update,
    notifies the user via a Notification object, and optionally triggers
    an admin-side status update.

    Args:
        request (HttpRequest): The HTTP request object.
        request_id (int): The ID of the BorrowRequest being returned.

    Returns:
        HttpResponseRedirect: Redirects the user to the notifications page.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data 
    borrow_request = get_object_or_404(BorrowRequest, id=request_id, user=user)
    borrow_request.status = 'book_returned'
    borrow_request.save()
    book=borrow_request.book
    print(f"Before return: Quantity={book.quantity}, is_available={book.is_available}")
    book.quantity += 1  
    book.is_available = True  
    book.save() 
    print(f"After return: Quantity={book.quantity}, is_available={book.is_available}")

    
    admin_instance = BorrowRequestAdmin(BorrowRequest, admin.site)
    admin_instance.update_status(request, request_id, 'book_returned')

    
    Notification.objects.create(
        user=borrow_request.user,
        message=f"You have successfully returned '{borrow_request.book.title}' book.",
        is_read=False
     )
    MemberActivity.objects.create(
        user=user,
        book=book,
        return_date=timezone.now(),
        status='book_returned'
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{borrow_request.user.id}",
        {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
    )
    messages.success(request, f"You have successfully returned '{borrow_request.book.title}' book.")

    return redirect('notification')

# @session_login_required
@csrf_exempt
def notification(request):
    """
    Handles the user notification view and triggers a Celery task for due date alerts.

    This view authenticates the user, triggers a Celery task (`send_due_date_notifications`)
    to check for upcoming due books, marks unread notifications as read, retrieves the latest
    50 notifications, and renders them along with books due in 3 days.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'notification.html' template with the due books and user notifications.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user, _ = user_data
    print(user)
    send_due_date_notifications(user.id)
    print(f"Task sent for user: {user.id}")
    today = timezone.now().date()
    Duedate = BorrowRequest.objects.filter(user=user, Duedate=today + timezone.timedelta(days=3))
    user_notifications_queryset = Notification.objects.filter(user=user).order_by('-timestamp')

    
    unread_notifications = user_notifications_queryset.filter(is_read=False)
    unread_notifications.update(is_read=True)
    user_notifications = user_notifications_queryset[:50]
    context = user_context_processor(request)
    html_content = render_to_string("notification.html", {**context,"due_books": Duedate,'user_notifications': user_notifications,'messages': messages.get_messages(request)  })  
    return HttpResponse(html_content)


def logout_view(request):
    """
    Handles user logout and updates logout time.

    This view authenticates the user using JWT, updates the `logout_time` in the `UserInfo` model 
    if the user is found, flushes the session, deletes authentication cookies, 
    and redirects the user to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the login page after logging out the user.
    """
    print('inside logout view')
    user_data = JWTAuthentication().authenticate(request)
    print(user_data)
    if user_data:  # Ensure authentication was successful
        user = user_data[0]  # Extract the User object
        print('Currently logged in user:', user)

        # **Update logout_time in UserInfo instead of creating new MemberActivity**
        try:
            user_info = UserInfo.objects.get(Username=user.Username)  # Ensure correct lookup
            user_info.logout_time = now()  # Update the logout time
            user_info.save(update_fields=['logout_time'])
            print(f'Updated logout time for {user.Username}: {user_info.logout_time}')
        except UserInfo.DoesNotExist:
            print('UserInfo not found for:', user.Username)  # Debugging
         
    request.session.flush()
    response = redirect(reverse('login'))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

def about(request):
    """
    Displays the About page.

    Authenticates the user using JWT, fetches unread notification count,
    and renders the 'about.html' template with context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered About page with context data.
    """
    user_data = JWTAuthentication().authenticate(request)
    user,_=user_data
    print("data",user_data)
    if not user_data:
        return redirect('login')
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('about.html',{**context})  
    return HttpResponse(html_content)

def privacy(request):
    """
    Displays the Privacy Policy page.

    Authenticates the user using JWT, fetches unread notification count,
    and renders the 'privacy.html' template with context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered Privacy Policy page with context data.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    user,_=user_data
    if not user_data:
        return redirect('login')
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('privacy.html',{**context})  
    return HttpResponse(html_content)

def terms(request):
    """
    Displays the Terms and Conditions page.

    Authenticates the user using JWT, fetches unread notification count,
    and renders the 'terms.html' template with context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered Terms and Conditions page with context data.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    user,_=user_data
    if not user_data:
        return redirect('login')
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('terms.html',{**context})  
    return HttpResponse(html_content)


def contact(request):
    """
    Displays the Contact Us page.

    Authenticates the user using JWT, fetches unread notification count,
    and renders the 'contactus.html' template with context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered Contact Us page with context data.
    """
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    user,_=user_data
    if not user_data:
        return redirect('login')
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('contactus.html',{**context})  
    return HttpResponse(html_content)
    