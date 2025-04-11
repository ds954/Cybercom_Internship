from rest_framework import serializers
from .models import UserInfo

"""
 Serializers in DRF are responsible for converting model instances to a format that can be easily rendered into JSON or other content types (serialization), and also for converting incoming data (like JSON from a request) back into model instances (deserialization).
"""
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

