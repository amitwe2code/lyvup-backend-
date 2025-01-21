from rest_framework import serializers
from .models import ConsentModel 

class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConsentModel
        fields=['id','user_id','consent_type','consent_status']

    
    # def create(self, validated_data):
    #     # यहाँ पर आप नए ConsentModel का एक उदाहरण बनाएँगे
    #     return ConsentModel.objects.create(**validated_data)
    # def update(self, instance, validated_data):
    #     # मौजूदा ConsentModel को अपडेट करें
    #     instance.user_id = validated_data.get('user_id', instance.user_id)
    #     instance.consent_type = validated_data.get('consent_type', instance.consent_type)
    #     instance.consent_status = validated_data.get('consent_status', instance.consent_status)
    #     instance.consent_date = validated_data.get('consent_date', instance.consent_date)
    #     instance.save()
    #     return instance