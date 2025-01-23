from rest_framework import serializers
from .models import GDPRRequestModel 

class GDPRSerializer(serializers.ModelSerializer):
    class Meta:
        model=GDPRRequestModel
        fields='__all__'
