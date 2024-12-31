from rest_framework import serializers
from .models import Intervention

from rest_framework import serializers
from .models import Intervention

class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = [
            'brand', 'activity', 'who', 'price', 'costs', 'send_reminder', 
            'id', 'intervention_type', 'language', 'name', 'label', 'description',
            'add_comment_option', 'show_completed', 'location', 'user_duration', 
            'duration_teamlead', 'duration_coach', 'coach_type', 'travel_time', 
            'url', 'file', 'upload_possible', 'intervention_description', 
            'intervention_name', 'show_in_tasks', 'indicate_when_completed',
        ]
    # todo = serializers.BooleanField()



# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:   
#         model = Language
#         fields = ['id', 'code', 'name']


# class InterventionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Intervention
#         fields = ['id', 'intervention_type', 'language', 'name', 'label', 'description']
