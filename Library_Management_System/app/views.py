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
from .models import Book,BorrowRequest,Notification
from .forms import ProfileForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages
from django.contrib import admin
from django.utils import timezone
from app.decoraters import session_login_required
from django.contrib.auth.decorators import login_required
from .tasks import send_due_date_notifications



def register_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm-password')

        if UserInfo.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email is already registered.'})
        try:
            validate_password(password)  
        except ValidationError as e:
            return render(request, 'register.html', {'error': e.messages}) 
        
        hashed_password=make_password(password)
        email_otp = generate_otp() 
        user=UserInfo.objects.create(Username=username,email=email,email_otp=email_otp,password=hashed_password)

        send_mail(
            'OTP Code',
            f'Your OTP for Registartion is: {email_otp}',
            settings.EMAIL_HOST_USER,
            [email]
        )
        return redirect('verify-otp', user_id=user.id) 
    else:
        pass

    return render(request,'register.html')

def verify_otp(request, user_id):
    user = get_object_or_404(UserInfo, id=user_id)

    if request.method == 'POST':
        email_otp = request.POST.get('email_otp','').strip()  
        if verifyotp(email_otp, user.email_otp): 
            user.is_email_verified = True  
            user.save()
            return redirect('/login/')  
        else:
            return render(request, 'Otp.html', {'error': 'Invalid OTP', 'user_id': user_id})  

    return render(request, 'Otp.html', {'user_id': user_id})  

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserInfo.objects.get(email=email)  
            if check_password(password, user.password):  
                request.session['user_id'] = user.id  
                return redirect('home')  
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except UserInfo.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})

    return render(request, 'login.html')

@login_required(login_url='/login/')
def home(request):
    from .models import UserInfo
    user_id = request.session.get('user_id')
    profile_user = None
    if user_id:
        profile_user = UserInfo.objects.get(id=user_id)

    return render(request, 'home.html', {'profile_user': profile_user})


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
            return render(request,'email.html', {'error': 'Email does not exist. Register first.'})

    return render(request,'email.html')

def otp_password(request, user_id):
    user = get_object_or_404(UserInfo, id=user_id)

    if request.method == 'POST':
        email_otp = request.POST.get('email_otp','').strip()  

        if verifyotp(email_otp, user.email_otp): 
            return redirect('reset_password', user_id=user.id)  
        else:
            return render(request, 'otp.html', {'error': 'Invalid OTP', 'user_id': user_id})  

    return render(request, 'otp.html', {'user_id': user_id})  


def reset_password(request, user_id):
    user = get_object_or_404(UserInfo, id=user_id)  
    if request.method == 'POST':
        password = request.POST.get('password') 
        confirm_password = request.POST.get('check-password')  
        try:
            validate_password(password)  # Check password strength
        except ValidationError as e:
            return render(request, 'reset_password.html', {'error': e.messages, 'user_id': user_id})

        if password == confirm_password:  
            user.password = make_password(password)  
            user.save()  
            return redirect('/login/')  
        else:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match or must be new.', 'user_id': user_id})

    return render(request, 'reset_password.html', {'user_id': user_id})

@session_login_required
def view_profile(request):
    user_id = request.session.get('user_id')

    # Fetch the user from the database
    user = get_object_or_404(UserInfo, id=user_id)

    

    return render(request, 'view_profile.html', { 'user': user})

@session_login_required
def edit_profile(request):
    user_id = request.session.get('user_id')
    user, created = UserInfo.objects.get_or_create(id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        phone = request.POST.get('phone_number')
        remove_picture = request.POST.get('remove_picture')


        # Update basic fields
        user.Username = username
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone

        # Handle form for file upload
        form = ProfileForm(request.POST, request.FILES, instance=user)

        # Remove photo if user clicked "Remove Photo"
        if remove_picture == 'true' :
            if user.profile_picture:
                # Delete the file from storage
                photo_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
                if os.path.isfile(photo_path):
                    os.remove(photo_path)
                user.profile_picture.delete(save=False)
                user.profile_picture = None
                
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        # Save user info and profile picture
        user.save()

        if form.is_valid():
            form.save()

        return redirect('edit_profile')  # Redirect to the same page after update

    else:
        form = ProfileForm(instance=user)

    return render(request, 'Edit_Profile.html', {'form': form, 'user': user})

@session_login_required
def home(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)
    return render(request,'home.html',{'user':user})

@session_login_required
def book_list(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'book.html', {'books': books})

@session_login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

@session_login_required
def search_books(request):
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

    return render(request, 'search_results.html', {
        'books': books,
        'query': query,
        'profile_user': profile_user,
    })

@session_login_required
def borrow_history(request):
    print(request.user)
    print(request.session.get('user_id'))

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect if user is not logged in

    user = get_object_or_404(UserInfo, id=user_id)
    borrow_requests = BorrowRequest.objects.filter(user=user)
    # print(borrow_requests)
    return render(request, 'borrow_history.html', {'borrow_requests': borrow_requests,'today': timezone.now().date()})
   
@session_login_required
def request_book(request, book_id):
        if request.method == "POST":
            user_id = request.session.get('user_id')
            user = get_object_or_404(UserInfo, id=user_id)  
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
            messages.success(request, "Your request has been submitted.")
        return redirect('notification')

@session_login_required
def returned_books(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

    borrow_requests = BorrowRequest.objects.filter(user=user, status='book_returned')

    return render(request, 'returned_books.html', {
        'borrow_requests': borrow_requests,
        'today': timezone.now().date()
    })

@session_login_required
def canceled_books(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

    borrow_requests = BorrowRequest.objects.filter(user=user, status='Cancel_Request')

    return render(request, 'canceled_books.html', {
        'borrow_requests': borrow_requests,
        'today': timezone.now().date()
    })

@session_login_required
def renewal_books(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

    borrow_requests = BorrowRequest.objects.filter(user=user, status='renew_accpect')
    print(borrow_requests)
    return render(request, 'renewal_books.html', {
        'borrow_requests': borrow_requests,
        'today': timezone.now().date()
    })

@session_login_required
def request_renewal(request,request_id):
    borrow_request = BorrowRequest.objects.get(id=request_id)
    borrow_request.status = 'renewal_requested'
    borrow_request.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{borrow_request.user.id}",
        {"type": "status_update", "status": borrow_request.status, "book": borrow_request.book.title}
    )
    return redirect('borrow_history')   

@session_login_required
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

     return redirect('notification')

@session_login_required
def return_book(request,request_id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id) 
    borrow_request = get_object_or_404(BorrowRequest, id=request_id, user=user)
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

    return redirect('notification')

@session_login_required
def notification(request):
    """Triggers Celery task and returns due books for the user."""

    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id) 
    print(user)
    # send_due_date_notifications.delay(user.id)
    send_due_date_notifications(user.id,repeat=60)
    print(f"Task sent for user: {user.id}")
    today = timezone.now().date()
    Duedate = BorrowRequest.objects.filter(user=user, Duedate=today + timezone.timedelta(days=3))
    user_notifications = Notification.objects.filter(user=user).order_by('-timestamp')[:50]
    
    return render(request, "notification.html", {"due_books": Duedate,'user_notifications': user_notifications})

def logout_view(request):
    a=request.session.flush()  # Clears all session data
    print(a)
    return redirect('login')
