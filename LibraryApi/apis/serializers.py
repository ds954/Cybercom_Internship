from rest_framework import serializers
from .models import apimodel

class apiSerializer(serializers.HyperlinkedModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = apimodel
        fields = ('username','name','email','password','password2','title', 'description')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = apimodel.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']

        )
        return user