from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from employee_data.models import CustomUser, StudentForm
from employee_data.functions import generate_otp, verifyotp, handle_uploaded_file
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# View for handling the student form submission
def student_form_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)  # Get form data and uploaded files
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])  # Save the uploaded file
            return HttpResponse("File uploaded successfully")  # Return success message
    else:  
        student = StudentForm()  # Create a blank form instance for GET request
        return render(request, "index.html", {'form': student})  # Render form in the template

# View for user registration and OTP generation
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get email from form input
        password=request.POST.get('password')
        email_otp = generate_otp()  # Generate a time-based OTP


        # Create a new user entry in the database with generated OTP
        user = CustomUser.objects.create(email=email, email_otp=email_otp,password=password)
        print(f"User created: ID={user.id}, Email={user.email}")  # Debugging print statement
        print(password)
    
        user.save()
        # Send OTP via email for verification
        send_mail(
            'Your OTP Code',
            f'Your OTP for verification is: {email_otp}',
            settings.EMAIL_HOST_USER,
            [email]
        )

        return redirect('verify_otp', user_id=user.id)  # Redirect to OTP verification page
    else:
        # Handle GET request (e.g., display an empty registration form)
        pass

    return render(request, "register.html")  # Render registration form

# View for OTP verification
def verify_otp(request, user_id):
    # Retrieve user from database or return 404 if not found
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        email_otp = request.POST.get('email_otp')  # OTP entered by the user

        if verifyotp(email_otp, user.email_otp):  # Check if entered OTP matches stored OTP
            user.is_email_verified = True  # Mark email as verified
            user.email_otp = None  # Clear OTP after successful verification
            user.save()
            return redirect('/login/')  # Redirect to homepage after successful verification
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP', 'user_id': user_id})  # Show error message

    return render(request, 'verify_otp.html', {'user_id': user_id})  # Render OTP verification form

# View for rendering the homepage
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        user = CustomUser.objects.get(email=email)
        if user.password == password:  # Compare plain text passwords
                login(request, user)  # Log in manually
                return redirect('/home/')
        else:
                messages.error(request, 'Incorrect password. Try again!')
                return redirect('/login/')
        

    return render(request, 'login.html')
 

def home(request):
    return render(request,'home.html')

def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)  # Get the existing user
            email_otp = generate_otp()

            # Store OTP in the user's database record
            user.email_otp = email_otp
            user.save()

            # Send OTP via email
            send_mail(
                'OTP For Reset Password',
                f'Your OTP code is: {email_otp}',
                settings.EMAIL_HOST_USER,
                [email]
            )
            return redirect('otp', user_id=user.id)  # Redirect to OTP verification page
        else:
            return render(request,'enter_email.html', {'error': 'Register'})


    return render(request, 'enter_email.html')

def otp_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        email_otp = request.POST.get('email_otp')  # OTP entered by the user

        if verifyotp(email_otp, user.email_otp):  # Check if entered OTP matches stored OTP
            return redirect('reset_password', user_id=user.id)   # Redirect to password reset page
        else:
            return render(request, 'otp.html', {'error': 'Invalid OTP', 'user_id': user_id})  # Show error message

    return render(request, 'otp.html', {'user_id': user_id})  # Render OTP verification form

def reset_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # Retrieve the user by ID

    if request.method == 'POST':
        password = request.POST.get('password')  # Get new password
        confirm_password = request.POST.get('check-password')  # Confirm password

        if password == confirm_password and password != user.password:  # Ensure new password is different
            user.password = password  # Store the plain text password
            user.save()  # Save the user with the updated password
            return redirect('/login/')  # Redirect to login after password reset
        else:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match or must be new.', 'user_id': user_id})

    return render(request, 'reset_password.html', {'user_id': user_id})

