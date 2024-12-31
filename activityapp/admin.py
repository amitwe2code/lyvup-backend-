from django.contrib import admin
from .models import ActivityActionType

class ActivityActionTypeAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'activity', 'amount', 'unit', 'key_activity', 'is_active', 'is_deleted', 'created_at', 'updated_at')

admin.site.register(ActivityActionType, ActivityActionTypeAdmin)
