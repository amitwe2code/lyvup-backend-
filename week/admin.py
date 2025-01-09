from django.contrib import admin
from .models import WeekModel

class WeekAdmin(admin.ModelAdmin):
    list_display=['week_no','program_id','activity_type','activity_id','activity_name']


admin.site.register(WeekModel,WeekAdmin)
# Register your models here.
