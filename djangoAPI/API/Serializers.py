from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This username is already taken."
            )
        ],
        error_messages={
            'min_length': "Username must be at least 3 characters long."
        }
    )

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
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

    
    def validate(self, attrs):
        # Get the request method (PATCH/PUT)
        request_method = self.context['request'].method.lower()
        print("Request method:", self.context['request'].method)
        print("Request data:", self.context['request'].data)
        print("Current instance:", getattr(self, 'instance', None))
            
        # Only validate on PATCH/PUT (not on GET)
        if request_method in ['patch', 'put']:
            instance = getattr(self, 'instance', None)
            
            if instance:  # Only for updates (not creation)
                restricted_fields = ['is_staff', 'is_superuser', 'is_active']
                
                # Get the request data (even if empty)
                request_data = self.context['request'].data
                
                # Check if any restricted field is in the request data
                for field in restricted_fields:
                    if field in request_data:
                        # Compare new value with current value
                        if str(getattr(instance, field)) != str(request_data[field]):
                            raise ValidationError({
                                field: f"You are not allowed to update {field}."
                            })
        
        return attrs
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        
        # Hide restricted fields in GET requests
        if request and request.method == 'GET':
            return fields
        
        # Allow validation (but not display) in PATCH/PUT
        fields.update({
            'is_staff': serializers.BooleanField(read_only=True),
            'is_superuser': serializers.BooleanField(read_only=True),
            'is_active': serializers.BooleanField(read_only=True),
        })
        return fields

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            
        ]
        # read_only_fields = ['is_staff', 'is_superuser', 'is_active']
