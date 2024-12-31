from rest_framework import serializers
from .models import ActivityActionType

class ActivityActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityActionType
        fields = ['id', 'activity_type', 'activity', 'amount', 'unit', 'key_activity', 'created_at', 'updated_at', 'is_active', 'is_deleted']
