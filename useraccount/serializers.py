from rest_framework import serializers
from userapp.serializers import UserSerializer
from account.serializers import AccountSerializer
from .models import UserAccountModel


class UserAccountSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    account=AccountSerializer()

    class Meta:
        model = UserAccountModel
        fields = ['id','user','account']

        
    def validate_is_active(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_active must be 0 or 1")
        return value

    def validate_is_deleted(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_deleted must be 0 or 1")
        return value