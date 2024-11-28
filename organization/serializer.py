from rest_framework import serializers
from .models import OrganizationModel



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = ['id', 'organization_name', 'description', 'created_by', 'is_active', 'is_deleted', 'created_at', 'updated_at']





