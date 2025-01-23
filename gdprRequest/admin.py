from django.contrib import admin
from .models import GDPRRequestModel

class GDPRAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','request_type','request_status')

admin.site.register(GDPRRequestModel, GDPRAdmin)