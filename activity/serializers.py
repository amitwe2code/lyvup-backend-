
from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    # updated_by = serializers.ReadOnlyField(source='updated_by.username')  # Read-only field
    # created_at = serializers.ReadOnlyField()  # Ensure it's read-only
    # updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Activity
        fields = [
            'id','activity_description', 'activity_name','activity_type','language','brand', 'completion_check','activity','who',
            'travel_time','send_reminder', 'add_comment_option', 'show_completed',
            'location', 'user_duration', 'coach_duration','teamlead_duration',
            'coach_type', 'url', 'amount', 'file', 'upload_possible',
             'show_in_task']
        

    def to_internal_value(self, data):
        for field_name, value in data.items():
            if value == "":
                field = self.fields.get(field_name)
                if field:
                    if isinstance(field, serializers.IntegerField):
                        data[field_name] = 0 
                    elif isinstance(field, serializers.BooleanField):
                        data[field_name] = False  

        return super().to_internal_value(data)

    
    def validate_user_duration(self, value):
        if value == "":
            return 0
        return value

    def validate_coach_duration(self, value):
        if value == "":
            return 0
        return value

    def validate_teamlead_duration(self, value):
        if value == "":
            return 0
        return value

 
        
    def validate_is_active(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("is_active must be 0 or 1")
        return value

    def validate_is_deleted(self, value):
       
        if value not in [0, 1]:
            raise serializers.ValidationError("is_deleted must be 0 or 1")
        return value
   