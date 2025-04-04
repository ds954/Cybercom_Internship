from account.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        """
        Meta class for RegisterSerializer.
        """
        model = User # Specifies the model to serialize (User)
        fields = ["email", "name", "password","confirm_password"]  # Specifies the fields to include in the serialization
       

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm_Password doesn't match.")
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
          raise serializers.ValidationError('user with this Email already exists.')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        user.is_active = False
        user.save()
        return user