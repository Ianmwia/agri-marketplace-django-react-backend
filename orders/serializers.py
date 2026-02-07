from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating and viewing orders

    '''
    image = serializers.ImageField()
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

        # only buyers can place orders
        if user.role != 'buyer':
            raise serializers.ValidationError('Only buyers can place orders')
        validated_data['buyer'] = user

        #get data from the db
        produce = validated_data['produce']
        order_quantity = validated_data['quantity']

        #check stock in the db
        if order_quantity > produce.quantity:
            raise serializers.ValidationError(
                f'Not Enough Stock Available: {produce.quantity}'
            )
        
        # reduce stock, and save it in the db
        produce.quantity -= order_quantity
        produce.save()
        
        return super().create(validated_data)