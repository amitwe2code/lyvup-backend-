from rest_framework import serializers
from .models import AccountModel




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountModel
        fields=['id','account_name','account_type','organization_id','team_leader_id' ,'language', 'created_at', 'updated_at']

    def validate_is_active(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_active must be 0 or 1")
        return value

    def validate_is_deleted(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_deleted must be 0 or 1")
        return value