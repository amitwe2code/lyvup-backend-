# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'from_id', 'from_type', 'to_id', 'to_type', 'message', 'is_read', 'created_at', 'is_active']
