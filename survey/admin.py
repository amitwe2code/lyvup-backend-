from django.contrib import admin
from .models import Intervention

class InterventionAdmin(admin.ModelAdmin):
    list_display = ('activity', 'intervention_type', 'language', 'price', 'costs', 'location') 
    search_fields = ('activity', 'location') 
    list_filter = ('intervention_type', 'language')  
admin.site.register(Intervention, InterventionAdmin)
