from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    # department_name = serializers.CharField(source='department.department_name', read_only=True)

    # Custom validation for name length
    name = serializers.CharField(min_length=3, error_messages={'min_length': "Name must be at least 3 characters long."})

    email = serializers.EmailField()

    def validate_email(self, value):
        if not value.endswith('@xyz.com'):
            raise serializers.ValidationError("Email must be from @xyz.com domain.")
        return value
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'joined_date', 'Designation']
