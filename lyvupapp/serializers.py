from rest_framework import serializers 
from django.contrib.auth import get_user_model

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

   
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs