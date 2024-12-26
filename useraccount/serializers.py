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

        
