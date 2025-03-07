from rest_framework import serializers
from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'Username', 'email', 'password', 'email_otp', 'is_email_verified']
        extra_kwargs = {'password': {'write_only': True}}
        
class UserInfoPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

