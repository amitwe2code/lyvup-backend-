from django.contrib import admin
from .models import Program


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'written_by', 'version', 'price', 'created_at', 'updated_at','is_active', 'is_deleted',)  # Add created_at and updated_at here
    search_fields = ('name', 'description', 'written_by', 'version')
    list_filter = ('created_at', 'updated_at')

admin.site.register(Program,ProgramAdmin)
