from django.contrib import admin
from .models import AccountModel

class AccountDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_name', 'account_type', 'organization_id', 'team_leader_id', 'language', 'is_active', 'is_deleted', 'created_at', 'updated_at')

admin.site.register(AccountModel, AccountDetailAdmin)
