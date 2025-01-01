from rest_framework import serializers
from .models import ActivityActionType

class ActivityActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityActionType
        fields = ['id', 'activity_type', 'activity', 'amount', 'unit', 'key_activity', 'created_at', 'updated_at']
    

    def validate_is_active(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_active must be 0 or 1")
        return value

    def validate_is_deleted(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_deleted must be 0 or 1")
        return value