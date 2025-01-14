from django.contrib import admin
from .models import ProgramActivityModel

class ProgramActivityAdmin(admin.ModelAdmin):
    list_display=['week_no','program_id','activity_type','activity_id','activity_name']


admin.site.register(ProgramActivityModel,ProgramActivityAdmin)
# Register your models here.
