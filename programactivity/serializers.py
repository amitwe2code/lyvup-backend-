from rest_framework import serializers
from .models import ProgramActivityModel


class ProgramActivitySerializer(serializers.ModelSerializer):
    class Meta :
        model=ProgramActivityModel
        fields='__all__'



    def validate_time(self, value):
        if value == "":
            return None
        return value