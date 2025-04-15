from rest_framework import generics
from .models import UserInfo
from .Serializers import UserSerializers

class UserCreateList(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers

class UserUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers
