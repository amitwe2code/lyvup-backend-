from rest_framework import serializers
from .models import Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'written_by', 'version', 'price','created_at', 'updated_at']
    def validate_is_active(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_active must be 0 or 1")
        return value

    def validate_is_deleted(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_deleted must be 0 or 1")
        return value