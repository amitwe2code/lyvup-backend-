from rest_framework import serializers
from .models import WeekModel


class WeekSerializer(serializers.ModelSerializer):
    class Meta :
        model=WeekModel
        fields='__all__'