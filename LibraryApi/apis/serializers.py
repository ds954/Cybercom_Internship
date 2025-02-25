from rest_framework import serializers
from .models import apimodel
from django.contrib.auth.hashers import make_password

class apiSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the `apimodel` that includes user registration fields.
    Handles password hashing and validation.
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)  # Second password field for confirmation

    class Meta:
        model = apimodel
        fields = ('username', 'name', 'email', 'password', 'password2', 'title', 'description')  # Fields to be serialized
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures password is not exposed in API responses
        }

    def validate(self, data):
        """
        Validates that password and password2 match.
        Raises a validation error if they don't.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        """
        Handles user creation with password hashing.
        Removes `password2` from the data before saving.
        """
        password = validated_data.pop('password')  # Get the password and remove it from validated_data
        hashed_password = make_password(password)  # Hash the password before storing

        # Create and return the user object
        user = apimodel.objects.create(
            username=validated_data.get('username'),
            name=validated_data['name'],
            email=validated_data['email'],
            password=hashed_password,
            title=validated_data.get('title'),
            description=validated_data.get('description')
        )
        return user

class ApiModelSerializer(serializers.ModelSerializer):
    """
    Serializer for handling `apimodel` title and description fields.
    Used for non-authentication related API interactions.
    """
    class Meta:
        model = apimodel
        fields = ('title', 'description')  # Specifies which fields to include in serialization