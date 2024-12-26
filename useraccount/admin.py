from django.contrib import admin

# Register your models here.
from .models import UserAccountModel

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account')

admin.site.register(UserAccountModel, UserAccountAdmin)
