from django.contrib import admin
from django import forms

from .models import Activity



class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity', 'activity_type', 'language','location') 
    search_fields = ('activity', 'location') 
    list_filter = ('activity_type', 'language')  
admin.site.register(Activity, ActivityAdmin)
