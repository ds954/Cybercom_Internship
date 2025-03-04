

from .models import BorrowRequest, Book
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .admin import BorrowRequestAdmin
from django.contrib import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import RefreshTokenModel
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timezone,timedelta
from .serializers import AppUserSerializer
from .serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .forms import UserRegistrationForm 

class AppUserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = AppUserSerializer(users, many=True)
        return Response(serializer.data)

User = get_user_model()

class GetAccessTokenView(APIView):
    def get(self, request):
        return render(request, 'get_access_token.html')
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        try:
            # Fetch refresh token from DB
            token_entry = RefreshTokenModel.objects.get(token=refresh_token)
            
            # Check if token is expired
            if token_entry.expires_at < now():
                return Response({"error": "Refresh token expired"}, status=401)
            
            # Generate new access token
            refresh = RefreshToken(token_entry.token)
            new_access_token = str(refresh.access_token)

            return Response({"access": new_access_token})

        except RefreshTokenModel.DoesNotExist:
            return Response({"error": "Invalid refresh token"}, status=400)
        
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            user.set_password(form.cleaned_data["password"])  # Hash password
            user.save()  # Save user with hashed password
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()  # Create an empty form for GET request
    return render(request, 'register.html', {'form': form})  # Pass form to template     
# class LoginView(APIView):
    # def post(self, request):
    #     serializer = LoginSerializer(data=request.data)
        
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=400)

    #     user = serializer.validated_data["user"]

    #     # Generate Refresh and Access Token
    #     refresh = RefreshToken.for_user(user)

    #     RefreshTokenModel.objects.create(
    #         user=user,
    #         token=str(refresh),
    #         expires_at=now() + timedelta(days=7)  # Set expiry for refresh token
    #     )

    #     return Response({
    #         "access": str(refresh.access_token),
    #         "refresh": str(refresh)
    #     })
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # Generate access & refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            RefreshTokenModel.objects.create(
            user=user,
            token=refresh,
            expires_at=now() + timedelta(days=7)  # Set expiry for refresh token
            )

            # Redirect to dashboard with secure cookies
            response = redirect('dashboard')
            response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax')

            return response
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')
    
@login_required
def dashboard_view(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    borrow_requests = BorrowRequest.objects.filter(user=request.user)
    books = Book.objects.all()
    today=datetime.now().date()
    return render(request, 'dashboard.html', {'borrow_requests': borrow_requests, 'books': books,'today':today})
    

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile_update.html', {'form': form})

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        try:
            token_entry = RefreshTokenModel.objects.get(token=refresh_token)
            token_entry.delete()  # Remove token from DB
            return Response({"message": "Logged out successfully."})
        except RefreshTokenModel.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)



def search(request):
    return render(request, 'dashboard.html')

def search_results(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type')
    results = []
    searched = False

    if query:
        searched = True
        if search_type == 'title':
            results = Book.objects.filter(title__icontains=query)
        elif search_type == 'author':
            results = Book.objects.filter(author__icontains=query)
        elif search_type == 'category':
            results = Book.objects.filter(category__icontains=query)

    return render(request, 'dashboard.html', {'results': results, 'searched': searched})

    

@login_required
def request_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        BorrowRequest.objects.create(user=request.user, book=book)
        return redirect('dashboard')
    else:
        return redirect('dashboard')
    
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
    return redirect('dashboard')   

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

     return redirect('dashboard')

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

    return redirect('dashboard')