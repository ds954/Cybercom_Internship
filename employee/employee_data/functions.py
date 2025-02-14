import pyotp

# Save uploaded file to the specified directory
def handle_uploaded_file(f):  
    with open('employee_data/static/upload/' + f.name, 'wb+') as destination:  
        for chunk in f.chunks():  # Read the file in chunks for efficient writing
            destination.write(chunk)  

# Generate a 6-digit OTP using time-based OTP (TOTP)
def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # OTP valid for 5 minutes
    return totp.now()  # Return the generated OTP

# Verify the generated OTP with the user's input
def verifyotp(otp, user_otp):
    return otp == user_otp  # Check if the provided OTP matches the generated one
