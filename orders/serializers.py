from rest_framework import serializers
from .models import Order
from .models import ProduceBatch

class OrderSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating and viewing orders

    '''
    image = serializers.ImageField(source='batch.produce.image', read_only=True)
    batch_name = serializers.ReadOnlyField(source='batch.batch_number')
    produce_name = serializers.ReadOnlyField(source='batch.produce.name')

    buyer_first_name = serializers.ReadOnlyField(source='buyer.first_name')
    buyer_last_name = serializers.ReadOnlyField(source='buyer.last_name')
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['buyer', 'status', 'total_price', 'mpesa_checkout_id', 'created_at', 'rejection_reason', 'total_amount',]

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
        batch = validated_data['batch']
        order_quantity = validated_data['quantity']

        validated_data['total_amount'] = batch.price_per_unit * order_quantity

        #check stock in the db
        if order_quantity > batch.quantity:
            raise serializers.ValidationError(
                f'Not Enough Stock Available: {batch.quantity}'
            )
        
        # reduce stock, and save it in the db
        batch.quantity -= order_quantity
        batch.save()
        
        return super().create(validated_data)
    
class ProduceBatchSerializer(serializers.ModelSerializer):
    produce_name = serializers.CharField(source='produce.name')
    farmer_first_name = serializers.CharField(source='produce.farmer.first_name')
    farmer_last_name = serializers.CharField(source='produce.farmer.last_name')
    produce_image = serializers.ImageField(source='produce.image', read_only=True)


    class Meta:
        model = ProduceBatch
        fields = ['id', 'batch_number', 'produce_name', 'quantity', 'price_per_unit', 'produce_image', 'farmer_first_name', 'farmer_last_name']

