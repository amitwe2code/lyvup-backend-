from django.contrib import admin
from django import forms

from .models import Intervention



class InterventionAdminForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = '__all__'
    
    # Optional validation if you want to enforce 1 and 0 only for these fields
    def clean_is_active(self):
        is_active = self.cleaned_data['is_active']
        if is_active not in [0, 1]:
            raise forms.ValidationError("is_active must be either 1 (True) or 0 (False)")
        return is_active

    def clean_is_deleted(self):
        is_deleted = self.cleaned_data['is_deleted']
        if is_deleted not in [0, 1]:
            raise forms.ValidationError("is_deleted must be either 1 (True) or 0 (False)")
        return is_deleted


class InterventionAdmin(admin.ModelAdmin):
    list_display = ('activity', 'intervention_type', 'language','location') 
    search_fields = ('activity', 'location') 
    list_filter = ('intervention_type', 'language')  
admin.site.register(Intervention, InterventionAdmin)
