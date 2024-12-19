from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.hashers import make_password
from django.conf import settings



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'name', 'email', 'user_type', 'profile_picture', 
                 'language_preference', 'status', 'is_active', 'is_deleted', 
                 'created_at', 'updated_at', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'user_type': {'required': False},
            'status': {'required': False},
            'is_active': {'required': False},
            'is_deleted': {'required': False},
            'language_preference': {'required': False},
            'profile_picture': {'required': False}
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        if 'language' in validated_data:
            validated_data['language_preference'] = validated_data.pop('language')
            
        return super().update(instance, validated_data)

    def validate_profile_picture(self, value):
        if value and value.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError('Image size should not exceed 5MB')
        return value
    
