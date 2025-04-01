from rest_framework import serializers
from .models import *

class DataSerializers(serializers.Serializer):
    class Meta:
        model:Department
        fields=['department']
 
