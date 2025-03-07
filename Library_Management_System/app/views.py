import os
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
from app.OtpGenration import generate_otp,verifyotp
from .models import UserInfo
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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

def home(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

    return render(request, 'home.html' ,{'user':user})  

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

def handle_uploaded_file(f):  
    upload_path = os.path.join('app/media/profile-pics', f.name)  # Ensure the directory exists
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)  # Create directories if not exist
    
    with open(upload_path, 'wb+') as destination:  
        for chunk in f.chunks():  # Read the file in chunks for efficient writing
            destination.write(chunk)
    
    return os.path.join('profile-pics', f.name)  # Return the relative path

# Function to Delete Profile Picture
def delete_profile_picture(user):
    if user.profile_picture:
        profile_picture_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)
        if os.path.exists(profile_picture_path):
            os.remove(profile_picture_path)
        user.profile_picture = None
        user.save()

def edit_profile(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        phone = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile-photo')
        remove_picture = request.POST.get('remove_picture')

        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.phone = phone

        # Remove Profile Picture if requested
        if remove_picture == "true":
            delete_profile_picture(user)

        # Save new profile picture if uploaded
        if profile_picture:
            profile_picture_path = handle_uploaded_file(profile_picture)  
            user.profile_picture = profile_picture_path  

        user.save()

        return redirect('home')

    return render(request, 'edit_profile.html', {'user': user})



