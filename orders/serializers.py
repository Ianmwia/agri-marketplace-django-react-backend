from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating and viewing orders

    '''
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['buyer', 'status', 'created_at']

    def create(self, validated_data):
        '''
        Docstring for create
        
        only buyers can create orders
        '''
        request = self.context['request']
        user = request.user
        if user.role != 'buyer':
            raise serializers.ValidationError('Only buyers can place orders')
        validated_data['buyer'] = user
        return super().create(validated_data)