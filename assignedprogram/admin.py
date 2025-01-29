from django.contrib import admin
from .models import AssignedProgramModel

class AssignedProgramAdmin(admin.ModelAdmin):
    list_display = ('id','company_id','account_id','assign_to','assign_type')

admin.site.register(AssignedProgramModel, AssignedProgramAdmin)