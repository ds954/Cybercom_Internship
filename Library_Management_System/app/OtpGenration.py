import pyotp
import datetime
from django.conf import settings
from django.core.mail import send_mail

def generate_otp():
    """
    Generate a 6-digit OTP using time-based OTP (TOTP)
    """
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # OTP valid for 5 minutes
    return totp.now()  # Return the generated OTP


def verifyotp(otp, user_otp):
    """
    Verify the generated OTP with the user's input
    """
    return otp == user_otp  # Check if the provided OTP matches the generated o