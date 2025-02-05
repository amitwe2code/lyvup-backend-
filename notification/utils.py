# notifications/utils.py
from .models import Notification

def create_notification(from_id, from_type, to_id, to_type, notification_type, message):
    # Notification create karna
    notification = Notification.objects.create(
        from_id=from_id,
        from_type=from_type,
        to_id=to_id,
        to_type=to_type,
        type=notification_type,
        message=message,
        is_read=False,
        is_active=True
    )
    return notification
