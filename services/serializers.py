from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service 
        fields = '__all__'
        read_only_fields = ['provider']

    def validate(self, attrs):
        user = self.context['request'].user
        selected_service = attrs.get('title')

        correct_field = {
        'animals': ['veterinarian', 'livestock_showman'],
        'soil': ['soil_technician'],
        'machinery': ['tractor_service'],
        }

        #check that a field officer has selected the right role
        if selected_service not in correct_field.get(user.field, []):
            raise serializers.ValidationError(
                f'You cannot select that role in the field '
            )
        return attrs
        
    def create(self, validated_data):
        #assign the logged in farmer as the creator
        validated_data['provider'] = self.context['request'].user
        return super().create(validated_data)
    