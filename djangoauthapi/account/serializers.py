from rest_framework import serializers
from .models import CustomUser,Book,BorrowRequest
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from account.utils import Util
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    class Meta:
        """
        Meta class for RegisterSerializer.
        """
        model = CustomUser  # Specifies the model to serialize (CustomUser)
        fields = ["email", "username", "password"]  # Specifies the fields to include in the serialization
        extra_kwargs = {"password": {"write_only": True}}  # Makes the password field write-only

    def create(self, validated_data):
        """
        Creates a new user instance.
        """
        user = CustomUser.objects.create_user(**validated_data)  # Creates a new user using the validated data
        return user  # Returns the created user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()  # Serializes the email field
    password = serializers.CharField(write_only=True)  # Serializes the password field (write-only)

    class Meta:
        model=CustomUser
        fields=['email','password']

class ProfileSerializer(serializers.Serializer):
    """
    Serializer for user profile.
    """
   
    class Meta:
        model=CustomUser
        fields=['email','username']

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for user profile.
    """
    password=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=CustomUser
        fields=['password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        user = self.context.get('user')  # Access the user object correctly

        if user:  # Check if the user object exists
            user.set_password(password)
            user.save()
        else:
            raise serializers.ValidationError("User not found in context.")

        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)

            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)

            link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
          

        else:
            raise ValidationError('You are not a Registered User')
        

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for user profile.
    """
    password=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=CustomUser
        fields=['password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        uid = self.context.get('uid')
        token = self.context.get('token')
        user = self.context.get('user')  # Access the user object correctly
        id = smart_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
             raise ValidationError('Token is not Valid or Expired')
        if user:  # Check if the user object exists
            user.set_password(password)
            user.save()
        else:
            raise serializers.ValidationError("User not found in context.")

        return attrs

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

class  BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields= ['id','title','is_available']

class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        modek=BorrowRequest
        fields=['id','user','book','status','IssuedDate','Duedate']

       


        
