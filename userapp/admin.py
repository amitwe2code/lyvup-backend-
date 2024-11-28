from django.contrib import admin
from .models import UserModel
# Register your models here.
class Useradmin(admin.ModelAdmin):
    list_display=('id','name','email','user_type','status', 'is_active', 'created_at', 'updated_at')




admin.site.register(UserModel,Useradmin)