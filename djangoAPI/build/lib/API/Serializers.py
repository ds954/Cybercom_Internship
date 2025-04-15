from rest_framework import serializers
from rest_framework.validators import UniqueValidator  
from .models import UserInfo

class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        validators=[
            UniqueValidator(
                queryset=UserInfo.objects.all(),
                message="This username is already taken."
            )
        ],
        error_messages={
            'min_length': "Username must be at least 3 characters long."
        }
    )

    firstname = serializers.CharField(
        min_length=3,
        error_messages={
            'min_length': "Firstname must be at least 3 characters long."
        }
    )

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=UserInfo.objects.all(),
                message="This email is already registered."
            )
        ],
        error_messages={
            'invalid': "Enter a valid email address."
        }
    )

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Email must be from @gmail.com domain.")
        return value

    class Meta:
        model = UserInfo
        fields = '__all__'
