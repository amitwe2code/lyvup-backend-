from rest_framework import serializers
from .models import AccountModel




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountModel
        fields=['id','account_name','account_type','organization_id','lead_provider_id' 'language', 'is_active', 'is_deleted', 'created_at', 'updated_at']

