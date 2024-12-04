from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.hashers import make_password
from django.conf import settings



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields=['id','name','email','user_type','profile_picture', 'language_preference', 'status', 'is_active', 'is_deleted', 'created_at', 'updated_at','password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}  
        }          

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)
    
    def validate_profile_picture(self, value):
        if value and value.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError('Image size should not exceed 5MB')
        return value
    
