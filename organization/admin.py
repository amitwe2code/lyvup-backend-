from django.contrib import admin
from .models import OrganizationModel

class organizationadmin(admin.ModelAdmin):
    list_display=('id', 'organization_name', 'description', 'created_by', 'is_active', 'is_deleted', 'created_at', 'updated_at')

admin.site.register(OrganizationModel,organizationadmin)   
              