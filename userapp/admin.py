from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel
from django.contrib.auth.models import User

class Useradmin(UserAdmin):
    list_display = ('id', 'name', 'email', 'user_type', 'status', 'is_active', 'created_at', 'updated_at')
    
    # arrange fields group wise.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('user_type', 'status', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2', 'user_type', 'status', 'is_active', 'is_staff'),
        }),
    )
    
    search_fields = ('email', 'name')
    ordering = ('email',)

admin.site.register(UserModel, Useradmin)