from rest_framework import serializers
from api.models import CustomUser

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