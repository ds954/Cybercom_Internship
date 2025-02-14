from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from user.models import Userinfo
from django.template import loader
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import pyotp

 

# Generate a 6-digit OTP using time-based OTP (TOTP)
def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # OTP valid for 5 minutes
    return totp.now()  # Return the generated OTP

# Verify the generated OTP with the user's input
def verifyotp(otp, user_otp):
    return otp == user_otp  # Check if the provided OTP matches the generated one


def register(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname') #Get firstname from register-page
        lastname=request.POST.get('lastname') #Get lastname from register-page
        email=request.POST.get('email') #Get email from register-page
        password=request.POST.get('password') #Get password from register-page
        email_otp=generate_otp() #store 6 digit otp in email_otp 

         # Create a new user entry in the database with generated OTP
        user = Userinfo.objects.create(email=email, email_otp=email_otp,password=password,firstname=firstname,lastname=lastname)
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
        

    return render(request,'register.html')

def verify_otp(request, user_id):
    # Retrieve user from database or return 404 if not found
    user = get_object_or_404(Userinfo, id=user_id)

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

        try:
            # Retrieve the user from the database
            user = Userinfo.objects.get(email=email)
            
            # Check if the provided password matches the stored one
            if user.password == password:
                # Manually create a session for the user
                request.session['user_id'] = user.id  # Store user ID in the session
                return redirect('/dashboard/')
            else:
                messages.error(request, 'Incorrect password. Try again!')
                return redirect('/login/')
        
        except Userinfo.DoesNotExist:
            messages.error(request, 'User does not exist!')
            return redirect('/login/')
    
    return render(request, 'login.html')
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/login/')  # Redirect to login if user is not logged in

    # Retrieve users for display (optional)
    users = Userinfo.objects.all()

    return render(request, 'dashboard.html', {'users': users})

def all_user(request):
 
    myuser = Userinfo.objects.all().values()
    template = loader.get_template('all_user.html')
    context = {
        'myuser': myuser,
    }
    return HttpResponse(template.render(context, request))

def add_user(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        college=request.POST.get('college_name')
        email=request.POST.get('email')
        print(f"Received: {firstname}, {lastname}, {college}, {email}") 
        user=Userinfo(firstname=firstname,lastname=lastname,college_name=college,email=email)
        user.save()

        return redirect('all_user')
    else:
        pass

    return render(request,'add.html')

def update_user(request,user_id):
    user=get_object_or_404(Userinfo,id=user_id)
    if request.method=='POST':
        user.firstname=request.POST.get('firstname')
        user.lastname=request.POST.get('lastname')
        user.college_name=request.POST.get('college_name')
        user.email=request.POST.get('email')
        user.save()

        return redirect('all_user')
    else:
        pass

    return render(request,'update.html' ,{'user':user})

def delete_user(request,user_id):
    user=get_object_or_404(Userinfo,id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect("all_user")


def logout_user(request):
    # Clear the user session by deleting the user_id from the session
    try:
        del request.session['user_id']  # Delete the user ID from the session to log the user out
    except KeyError:
        pass  # If 'user_id' doesn't exist, nothing happens

    # Redirect to the login page after logging out
    return redirect('/login/')