from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

User = get_user_model()  # This ensures the correct user model (CustomUser) is used.

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Using the CustomUser model from the account app
        fields = ["id", "email", "username"]  # Customize this list based on your needs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        data["user"] = user
        return data
