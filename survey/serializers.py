from rest_framework import serializers
from .models import Intervention

from rest_framework import serializers
from .models import Intervention

class InterventionSerializer(serializers.ModelSerializer):
    # updated_by = serializers.ReadOnlyField(source='updated_by.username')  # Read-only field
    # created_at = serializers.ReadOnlyField()  # Ensure it's read-only
    # updated_at = serializers.ReadOnlyField()
    class Meta:
        model = Intervention
        fields = [
            'id','intervention_type','language', 'activity', 'brand', 'who',
            'activity_type', 'completion_check', 'send_reminder', 'add_comment_option', 'show_completed',
            'location', 'user_duration', 'duration_coach',
            'coach_type', 'url', 'amount', 'file', 'upload_possible',
            'intervention_description', 'intervention_name', 'show_in_tasks']
    def validate_is_active(self, value):
        # value is either 1 (active) or 0 (inactive)
        if value not in [0, 1]:
            raise serializers.ValidationError("is_active must be 0 or 1")
        return value

    def validate_is_deleted(self, value):
        # value is either 0 (not deleted) or 1 (deleted)
        if value not in [0, 1]:
            raise serializers.ValidationError("is_deleted must be 0 or 1")
        return value
     # todo = serializers.BooleanField()



# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:   
#         model = Language
#         fields = ['id', 'code', 'name']


# class InterventionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Intervention
#         fields = ['id', 'intervention_type', 'language', 'name', 'label', 'description']
