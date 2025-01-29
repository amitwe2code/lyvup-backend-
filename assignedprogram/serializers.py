from rest_framework import serializers
from .models import AssignedProgramModel

class AssignedProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model=AssignedProgramModel
        fields='__all__'