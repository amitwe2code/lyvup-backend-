from django.contrib import admin
from .models import ConsentModel

class ConsentAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','consent_type','consent_status')

admin.site.register(ConsentModel, ConsentAdmin)