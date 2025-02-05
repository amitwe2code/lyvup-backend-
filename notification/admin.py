from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id','type', 'from_id', 'from_type', 'to_id', 'to_type', 'message', 'is_read', 'created_at', 'is_active')

admin.site.register(Notification, NotificationAdmin)