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


def admin_profile_view(request):
    user = request.user  
    admin_profile = User.objects.get(username=user)  

    html_content=render_to_string('admin/admin_profile.html', {'admin_profile': admin_profile})
    return HttpResponse(html_content)
@csrf_exempt
def admin_profile_edit(request):
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
from django.db.models import Count

def borrowed_books_report(request):
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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="borrowed_books_report.pdf"'

    CUSTOM_HEIGHT=3300
    CUSTOM_WIDTH=3000
    CUSTOM_SIZE=(CUSTOM_HEIGHT,CUSTOM_WIDTH)
    p = canvas.Canvas(response, pagesize=CUSTOM_SIZE)
    width, height = CUSTOM_SIZE

    p.setFont("Helvetica-Bold", 24)
    p.drawString(1000, height - 50, "Borrowed Books Report")

    generated_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    p.setFont("Helvetica", 22)
    p.drawString(1000, height - 70, f"Generated on: {generated_time}")

    borrowed_books = BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect','renewal_requested'])
    total_borrowed_books=borrowed_books.count()
    print(total_borrowed_books)
    most_borrowed = (
        BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect'])
        .values('book__id', 'book__title', 'book__author')
        .annotate(borrow_count=Count('id'))
        .order_by('-borrow_count')
        .first()
    )

    # Display most borrowed book details
    if most_borrowed:
        p.setFont('Helvetica-Bold', 22)
        p.drawString(90, height - 100, f"Total Number of Borrowed Books: {total_borrowed_books}")
        p.setFont('Helvetica-Bold', 22)
        p.drawString(90, height - 130, "Most Borrowed Book:")
        p.setFont('Helvetica', 22)
        p.drawString(90, height - 160, f"Title: {most_borrowed['book__title']}")
        p.drawString(90, height - 190, f"Author: {most_borrowed['book__author']}")
        p.drawString(90, height - 220, f"Times Borrowed: {most_borrowed['borrow_count']}")

    # Fetch data
    borrowed_books = BorrowRequest.objects.filter(status__in=['accepted','renew_accpect'])

    data = [['Member ID','Borrowed By', 'Email','Contact No', 'Book ID', 'Title','Author', 'Issued Date', 'Due Date','Status','Return Status','Renewal Requested','Renewal Requested Date','Approve/Reject']]
    for req in borrowed_books:
        data.append([req.user.id,req.user.Username,req.user.email,req.user.phone,req.book.id,req.book.title, req.book.author,str(req.IssuedDate), str(req.Duedate),req.status,
        
         'Yes' if (req.status in ['accepted', 'renewal_accepted'] and req.Duedate < datetime.now().date()) or req.status == 'book_returned' else 'No',

            'Yes' if req.status in ['renewal_requested', 'renew_accpect'] else 'No',

            req.renewalrequests_set.first().request_date if req.status in ['renewal_requested', 'renew_accpect'] and req.renewalrequests_set.exists() else 'N/A',

            'Approved' if req.status == 'renew_accpect' else 'Rejected' if req.status == 'renew_reject' else 'Pending' if req.status == 'renewal_requested' else 'N/A'
        ])
                     

        # if req.status == 'accepted' or req.status == 'renewal_accepted' and req.Duedate < datetime.now().date() or req.status == 'book_returned':
        #     data.append('Yes')
        # else:
        #     data.append('No')    

        # if req.status == 'renewal_requested' or req.status == 'renew_accpect':
        #     data.append('Yes')
        #     # if req.renewalrequests_set.first:
        #     #     data.append(req.renewalrequests_set.first.request_date)
        #     # else:
        #     #     data.append('N/A')
        # else:
        #     data.append('No')
        #     data.append('N/A')

        # if req.status == 'renew_accpect':
        #     data.append('Approved')
        # elif req.status == 'renew_reject':
        #     data.append('Rejected') 
        # elif req.status == 'renewal_requested':
        #     data.append('Pending')    
        # else:
        #     data.append('N/A')            




    # Create table
    table = Table(data, colWidths=[100, 200, 300, 200, 100, 400, 300, 150, 150, 200, 200, 300, 300, 300], rowHeights=[50,50,50,50,50,50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 22),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 22),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 90, height - 600)


    user_borrow_stats = (
        UserInfo.objects.annotate(
            borrow_count=Count('borrowrequest', filter=Q(borrowrequest__status__in=['accepted', 'renew_accpect']))
        ).values('id', 'Username', 'borrow_count')
    )
    data1=[['User ID','Username','No of Books Borrowed']]
    for user in user_borrow_stats:
        data1.append([user['id'],user['Username'],user['borrow_count']])

    table1=Table(data1,colWidths=[200,200,300],rowHeights=[50]*12)
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 22),
    ]))

    p.showPage()
    p.setFont("Helvetica-Bold", 24)
    p.drawString(200,height-50,"User Borrow Statistics")
    table1.wrapOn(p,CUSTOM_WIDTH,height-1000)
    table1.drawOn(p, 50, height - 800)

    p.save()
    return response


def overdue_books_report(request):
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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="overdue_books_report.pdf"'

    CUSTOM_WIDTH=2500
    CUSTOM_HEIGHT=1500
    CUSTOM_SIZE=(CUSTOM_WIDTH,CUSTOM_HEIGHT)
    p = canvas.Canvas(response, pagesize=CUSTOM_SIZE)
    width, height = CUSTOM_SIZE

    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, height - 50, "Overdue Books Report")

    generated_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    p.setFont("Helvetica", 20)
    p.drawString(100, height - 80, f"Generated on: {generated_time}")

    # Get overdue books (due date before today and not returned)
    overdue_books = BorrowRequest.objects.filter(status__in=['accepted','renew_accpect','renewal_requested'],Duedate__lt=now().date())

  
    total_overdue_books = overdue_books.count()
    p.setFont("Helvetica",20)
    p.drawString(100, height - 100, f"Total Overdue Books: {total_overdue_books}")
    print('total_overdue_books:',total_overdue_books)

    data = [['Member ID','Borrowed By','Email','Contact No','Book ID','Title','Author', 'Issued Date', 'Due Date','Status','Overdue Days']]
    for req in overdue_books:
        overdue_days=(datetime.now().date() - req.Duedate).days
        data.append([req.user.id,req.user.Username,req.user.email,req.user.phone,req.book.id,req.book.title,req.book.author, str(req.IssuedDate), str(req.Duedate),req.status,overdue_days])
        print(f"Overdue Days Calculation: {(datetime.now().date() - req.Duedate).days}")
    print("Table Data:")
    for row in data:
        print(row)    

    table = Table(data, colWidths=[200,200, 300, 200, 200,200,200,200,200,200,200],rowHeights=[40]*2)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE',(0,0),(-1,-1),18)
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 100, height - 200)

    p.showPage()
    p.save()
    return response


def member_activities_report(request):
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
        last_activity = MemberActivity.objects.filter(user=user).order_by('-login_time').first()
        
        print(last_activity)
        user_data.append({
            'user': user,
            'borrow_count': borrow_count,
            'notification_count': notification_count,
            'last_login': last_activity.login_time if last_activity else None,
            'last_logout': last_activity.logout_time if last_activity else None,
        })
        member_activities = MemberActivity.objects.select_related('user', 'book').all()
        


        total_return_count += return_count
        total_cancel_count += cancel_count
        total_pending_count += pending_count
        total_rejected_count += rejected_count
        total_accepted_count += accepted_count
        total_renewal_request_count += renewal_request_count
        total_renewal_rejected_count+= renewal_rejected_count
        total_renewal_accepted_count+= renewal_accepted_count

    
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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="member_activities_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Member Activities Report")

    generated_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    p.setFont("Helvetica", 12)
    p.drawString(200, height - 70, f"Generated on: {generated_time}")

    # First table: User basic details
    users = UserInfo.objects.all()
    user_data = [['Username', 'Email', 'Firstname', 'Lastname', 'Phone Number', 'Date of registration']]

    for user in users:
        user_data.append([
            user.Username, user.email, user.firstname, user.lastname, user.phone, user.created_at.strftime('%Y-%m-%d')
        ])

    table = Table(user_data, colWidths=[50, 150, 50, 50, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(p, width - 100, height - 400)
    table.drawOn(p, 50, height - 100 - 250)

    # Second table: Borrow Requests and Notifications
    data = [['Username', 'Email', 'Borrow Requests', 'Notifications']]
    for user in users:
        borrow_count = BorrowRequest.objects.filter(user=user).count()
        notification_count = Notification.objects.filter(user=user).count()

        data.append([user.Username, user.email, borrow_count, notification_count])

    table1 = Table(data, colWidths=[100, 200, 100, 100])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Start a new page before drawing the second table
    p.showPage()
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Borrow and Notification Summary")

    table1.wrapOn(p, width - 100, height - 400)
    table1.drawOn(p, 50, height - 100 - 200)

    # Third table: Detailed user activities (borrow history)
    activity_data = [['Borrowed By', 'Title', 'Status', 'Issued Date', 'Due Date']]
    borrow_requests = BorrowRequest.objects.all()

    for request_obj in borrow_requests:
        activity_data.append([
            request_obj.user.Username,
            request_obj.book.title,
            request_obj.status,
            request_obj.IssuedDate.strftime('%Y-%m-%d') if request_obj.IssuedDate else 'N/A',
            request_obj.Duedate.strftime('%Y-%m-%d')
        ])

    table2 = Table(activity_data, colWidths=[50, 200, 100, 90, 90])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Start another page before drawing the third table
    p.showPage()
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Detailed Borrow Activity")
    # p.drawString(f'Total Returned Books: {}')

    table2.wrapOn(p, width - 100, height - 400)
    table2.drawOn(p, 50, height - 100 - 400)

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
    request.session.flush()
    response = redirect(reverse('login'))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def custom_admin_dashboard(request):
    users = UserInfo.objects.all()
    books = Book.objects.all()
    borrow_requests = BorrowRequest.objects.select_related('user', 'book').all()
    recent_notifications = Notification.objects.order_by('-timestamp')
    total_issued_books = BorrowRequest.objects.filter(status__in =['accepted','renew_accpect']).count()
    total_pending_borrow_requests = BorrowRequest.objects.filter(status='pending').count()
    total_pending_renewal_requests = BorrowRequest.objects.filter(status='renewal_requested').count()
    total_returned_books = BorrowRequest.objects.filter(status='book_returned').count()
    total_not_returned_books = BorrowRequest.objects.filter(status__in =['accepted','renew_accpect','renewal_requested'],Duedate__lt=now().date()).count()
    total_not_returned_bookss = BorrowRequest.objects.filter(status__in =['accepted','renew_accpect','renewal_requested'],Duedate__lt=now())
    print("non returned books",total_not_returned_bookss)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        filter_borrow_requests = borrow_requests.filter(IssuedDate__range=(start_date, end_date))
        filter_total_issued_books = BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect'], IssuedDate__range=(start_date, end_date)).count()
        filter_total_pending_borrow_requests = BorrowRequest.objects.filter(status='pending', IssuedDate__range=(start_date, end_date)).count()
        filter_total_pending_renewal_requests = BorrowRequest.objects.filter(status='renewal_requested', IssuedDate__range=(start_date, end_date)).count()
        filter_total_returned_books = BorrowRequest.objects.filter(status='book_returned', IssuedDate__range=(start_date, end_date)).count()
        filter_total_not_returned_books = BorrowRequest.objects.filter(status__in=['accepted', 'renew_accpect'], IssuedDate__range=(start_date, end_date)).count()
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
    books = Book.objects.all()
    books_html = render_to_string('admin/books.html', {'books': books})
    return HttpResponse(books_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def custom_book_add(request):
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
        return redirect('custom_books')

    form_html = render_to_string('admin/book_add.html')
    return HttpResponse(form_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_borrow_request(request):
    borrow_requests=BorrowRequest.objects.filter(status__in =['pending'])
    borrow_request_html = render_to_string('admin/borrow_request.html', {
        'borrow_requests': borrow_requests,
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_pending_renewal_request(request):
    borrow_requests=BorrowRequest.objects.filter(status__in =['renewal_requested'])
    borrow_request_html = render_to_string('admin/pending_renewal.html', {
        'borrow_requests': borrow_requests,   
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_issued_book(request):
    borrow_requests=BorrowRequest.objects.filter(status__in =['accepted','renew_accpect'])
    borrow_request_html = render_to_string('admin/issued_book.html', {
        'borrow_requests': borrow_requests, 
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_returned_book(request):
    borrow_requests=BorrowRequest.objects.filter(status='book_returned')
    borrow_request_html = render_to_string('admin/returned_book.html', {
        'borrow_requests': borrow_requests,  
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_borrow_history(request):
    borrow_requests = BorrowRequest.objects.select_related('user').all()
    borrow_request_html = render_to_string('admin/borrow_history.html', {
        'borrow_requests': borrow_requests,  
    })
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_not_returned_book(request):
    borrow_requests = BorrowRequest.objects.select_related('user').filter(status__in=['accepted','renew_accpect','renewal_requested'],Duedate__lt=now().date())
    borrow_request_html = render_to_string('admin/non_returned_book.html', {
        'borrow_requests': borrow_requests,'today': timezone.now().date()
        })  
    return HttpResponse(borrow_request_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user(request):
    users = UserInfo.objects.all()
    user_html = render_to_string('admin/user.html', {
        'users': users,
    })
    return HttpResponse(user_html)
    
@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_members(request):
    users = UserInfo.objects.all()
    user_html = render_to_string('admin/manage_members.html', {'users': users})
    return HttpResponse(user_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_member(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
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
    print(f"edit_member called with member_id: {member_id}")
    member = get_object_or_404(UserInfo, id=member_id)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('manage_members')  # Redirect to members list after updating
    else:
        form = UserForm(instance=member)
    user_html = render_to_string('admin/edit_member.html', {'form': form})
    return HttpResponse(user_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_member(request, user_id):
    user = get_object_or_404(UserInfo, id=user_id)
    user.delete()
    return redirect('manage_members')

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_books(request):
      print("manage books called")
      books = Book.objects.all()
      book_html = render_to_string('admin/manage_books.html', {'books':books})
      return HttpResponse(book_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    print('inside add_book')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm()
    book_html = render_to_string('admin/add_book.html', {'form': form})
    return HttpResponse(book_html)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_book(request, book_id):
    print(f"edit_member called with member_id: {book_id}")
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage_books')  
    else:
        form = BookForm(instance=book)
    book_html = render_to_string('admin/edit_book.html', {'form': form})
    return HttpResponse(book_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
   
    return redirect('manage_books')

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def bulk_upload_books(request):
    if request.method == "POST":
        form = BookBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.process_file()
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
    recent_notifications = Notification.objects.order_by('-timestamp')
    user_html = render_to_string('admin/notification.html', {
        'notifications': recent_notifications
       
    })
    return HttpResponse(user_html)

@login_required
@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def update_borrow_request_status(request, request_id):
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
    print("inside register view")
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm-password')

        if UserInfo.objects.filter(email=email).exists():
             html_content = render_to_string( 'register.html', {'error': 'Email is already registered.'})  
             return HttpResponse(html_content)
        if User.objects.filter(username=username).exists():
             html_content = render_to_string( 'register.html', {'error': 'Username is already registered.'})  
             return HttpResponse(html_content)

           
        try:
            validate_password(password,confirm_password)  
        except ValidationError as e:
             html_content = render_to_string('register.html', {'error': e.messages})  
             return HttpResponse(html_content)
           
        
        hashed_password=make_password(password)
        email_otp = generate_otp() 
        print(email_otp)
        user=UserInfo.objects.create(Username=username,email=email,email_otp=email_otp,password=hashed_password)

        send_mail(
            'OTP Code',
            f'Your OTP for Registartion is: {email_otp}',
            settings.EMAIL_HOST_USER,
            [email]
        )
        return redirect('verify-otp', user_id=user.id)  # Redirect to OTP verification page

    else:
        pass

    html_content = render_to_string('register.html')  
    return HttpResponse(html_content)

@csrf_exempt
def verify_otp(request, user_id):
    user = JWTAuthentication().authenticate(request)
    user = UserInfo.objects.get(id=user_id)
    if request.method == 'POST':
        email_otp = request.POST.get('email_otp','').strip()  
        if verifyotp(email_otp, user.email_otp): 
            user.is_email_verified = True  
            user.save()
            return redirect('/')  
        else:
            html_content = render_to_string('Otp.html', {'error': 'Invalid OTP', 'user_id': user_id})  
            return HttpResponse(html_content)
    html_content = render_to_string('Otp.html', {'user_id': user_id})  
    return HttpResponse(html_content)

# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             user = UserInfo.objects.get(email=email)  
#             if check_password(password, user.password):  
#                 request.session['user_id'] = user.id  
#                 return redirect('home')  
#             else:
#                 return render(request, 'login.html', {'error': 'Invalid credentials'})
#         except UserInfo.DoesNotExist:
#             return render(request, 'login.html', {'error': 'User does not exist'})

#     return render(request, 'login.html')


@csrf_exempt
def login_view(request):
    
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
                
                
                # print("User",user_info)
                # MemberActivity.objects.create(user=user_info, login_time=now())

                response = redirect('home')
                response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax',max_age=settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'].total_seconds(),)
                response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Lax',max_age=settings.JWT_AUTH['JWT_REFRESH_TOKEN_LIFETIME'].total_seconds())
                return response
            else:

                html_content = render_to_string('login.html', {'error': 'Invalid credentials'})
                return HttpResponse(html_content)

        html_content = render_to_string('login.html')
        return HttpResponse(html_content)
# @csrf_exempt
# def login_view(request):
#     print("Inside login_view")
#     print(request.COOKIES)  
#     print(request.session.items()) 
#     print(f"Request Path: {request.path}")
#     if request.method == 'POST':
#         print("post request")
        
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             user = UserInfo.objects.get(email=email)  
#             if check_password(password, user.password):  
#                 access_token_payload = {
#                     'email': user.email,
#                     'exp': datetime.now() + settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'],
#                     'iat': int(time.time()),
#                 }
#                 access_token = jwt.encode(access_token_payload, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithm=settings.JWT_AUTH['JWT_ALGORITHM'])

#                 refresh_token_payload = {
#                     'email': user.email,
#                     'exp': datetime.now() + settings.JWT_AUTH['JWT_REFRESH_TOKEN_LIFETIME'],
#                     'iat': int(time.time()),
#                 }
#                 refresh_token = jwt.encode(refresh_token_payload, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithm=settings.JWT_AUTH['JWT_ALGORITHM'])

#                 RefreshTokenStore.objects.filter(user=user).delete()
#                 RefreshTokenStore.objects.create(user=user, token=refresh_token)

#                 response = redirect('home')
#                 response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax',max_age=settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'].total_seconds(),)
#                 response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Lax',max_age=settings.JWT_AUTH['JWT_REFRESH_TOKEN_LIFETIME'].total_seconds())
#                 return response
#             else:
#                 html_content = render_to_string('login.html', {'error': 'Invalid credentials'})  
#                 return HttpResponse(html_content)
                
#         except UserInfo.DoesNotExist:
#             html_content = render_to_string('login.html', {'error': 'User not found'})  
#             return HttpResponse(html_content)
        
#     html_content = render_to_string('login.html')  
#     return HttpResponse(html_content)



# def refresh_token_view(request):
#     refresh_token = request.COOKIES.get('refresh_token')
#     print("refresh_token: ",refresh_token)
#     if not refresh_token:
#         messages.error(request, "Session expired. Please log in again.")
#         return redirect('login')

#     try:
#         payload = jwt.decode(
#             refresh_token, 
#             settings.JWT_AUTH['JWT_SECRET_KEY'], 
#             algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']]
#         )
#         user = UserInfo.objects.get(email=payload['email'])

#         refresh_token_obj = RefreshTokenStore.objects.filter(user=user, token=refresh_token).first()
#         if not refresh_token_obj:
#             messages.error(request, "Session expired. Please log in again.")
#             return redirect('login')

#         access_token_payload = {
#             'email': user.email,
#             'exp': datetime.now() + settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'],
#             'iat': datetime.now(),
#         }
#         access_token = jwt.encode(
#             access_token_payload, 
#             settings.JWT_AUTH['JWT_SECRET_KEY'], 
#             algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
#         )

#         response = redirect('home')
#         response.set_cookie(
#             'access_token', access_token, httponly=True, secure=True, samesite='Lax',
#             max_age=settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'].total_seconds()
#         )
#         return response

#     except (jwt.ExpiredSignatureError, jwt.DecodeError, UserInfo.DoesNotExist):
#         messages.error(request, "Session expired. Please log in again.")
#         return redirect('login')
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



# @login_required(login_url='/login/')
# def home(request):
#     from .models import UserInfo
#     user_id = request.session.get('user_id')
#     profile_user = None
#     if user_id:
#         profile_user = UserInfo.objects.get(id=user_id)

#     return render(request, 'home.html', {'profile_user': profile_user})

@csrf_exempt
def email(request):
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
        remove_picture = request.POST.get('remove_picture','true')
        print("Remove Picture Value:", remove_picture) 

        # Update basic fields
        user.Username = username
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone

        # Handle form for file upload
        form = ProfileForm(request.POST, request.FILES, instance=user)

        # Remove photo if user clicked "Remove Photo"
        if remove_picture == 'true' :
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

        # Save user info and profile picture
        # user.save()
       
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
            'returned_count': returned_count,'notification_count': notification_count})  
    return HttpResponse(html_content)
  

# @session_login_required
def book_list(request):
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    books = Book.objects.all()  # Fetch all books from the database
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    context.update({'notification_count': notification_count})
    html_content = render_to_string('book.html', {**context,'books': books})  
    return HttpResponse(html_content)

# @session_login_required
def book_detail(request, book_id):
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
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    user,_=user_data
    if not user_data:
        return redirect('login')
    query = request.GET.get('q', '').strip()  # get search query from URL params
    books = []

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)  # Add more fields as necessary
        )

    user_id = request.session.get('user_id')
    profile_user = None
    if user_id:
        profile_user = UserInfo.objects.get(id=user_id)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    context.update({'notification_count': notification_count})
    html_content = render_to_string('search_results.html', {**context,
        'books': books,
        'query': query,
        'profile_user': profile_user})  
    return HttpResponse(html_content)

# @session_login_required
def borrow_history(request):
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
    user_data = JWTAuthentication().authenticate(request)
    user,_=user_data
    print("data",user_data)
    if not user:
        return redirect('login')
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    context.update({'notification_count': notification_count})
   
    borrow_requests = BorrowRequest.objects.filter(user=user)
    html_content = render_to_string('user_book.html', {**context,'borrow_requests': borrow_requests})  
    return HttpResponse(html_content)


# @session_login_required
def user_duebook(request):
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    print(user)
    borrow_requests = BorrowRequest.objects.filter(user=user)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})

    html_content = render_to_string('user_duebook.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)

# @session_login_required
def pending_renewal(request):
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    borrow_requests = BorrowRequest.objects.filter(user=user)
   
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('pending_renewals.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)

def pending_request(request):
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    user,_=user_data
    borrow_requests = BorrowRequest.objects.filter(user=user)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('pending_request.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)


# @session_login_required
def returned_book(request):
    user_data = JWTAuthentication().authenticate(request)
    print("data",user_data)
    if not user_data:
        return redirect('login')
    
    user,_ =user_data
    borrow_requests = BorrowRequest.objects.filter(user=user)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    context = user_context_processor(request) 
    context.update({'notification_count': notification_count})
    html_content = render_to_string('return_books.html', {**context,'borrow_requests': borrow_requests,'today': timezone.now().date()})  
    return HttpResponse(html_content)

# @session_login_required
@csrf_exempt
def request_book(request, book_id):
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
                IssuedDate=timezone.now(),
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
        return HttpResponseRedirect(reverse('notification'))

# @session_login_required
@csrf_exempt
def returned_books(request):
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
    """Triggers Celery task and returns due books for the user."""
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
    # return render(request, "notification.html", {
    #     "due_books": Duedate,
    #     "user_notifications": user_notifications
    # })


def logout_view(request):
    if request.user.is_authenticated:
        user_info = JWTAuthentication().authenticate(request)
        if user_info:
           MemberActivity.objects.filter(user=user_info,logout_time__isnull=True).update(logout_time=now())
        # logout(request)   
    request.session.flush()
    response = redirect(reverse('login'))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

def about(request):
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
    