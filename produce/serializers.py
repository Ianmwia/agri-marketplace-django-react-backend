from rest_framework import serializers
from .models import Category, Produce, ProduceBatch
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceBatch
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProduceSerializer(serializers.ModelSerializer):
    #accept input by email not fk id
    image = serializers.ImageField(required=False, allow_null=True)
    batches = BatchSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')

    quantity = serializers.IntegerField(write_only=True)
    price_per_unit = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)
    batch_number = serializers.CharField(write_only=True)
    unit = serializers.CharField(write_only=True, required=False, default='kg')

    category = serializers.CharField()

    farmer_name = serializers.ReadOnlyField(source='farmer.first_name')
    farmer = serializers.SlugRelatedField(
        slug_field='email',
        #queryset=User.objects.all(),
        required = False,
        read_only = True,
        style = {'base_template': 'hidden.html'}
    )

    # category = serializers.CharField()
    class Meta:
        model = Produce
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != 'farmer':
            raise serializers.ValidationError('only farmers can create produce')
        
        quantity = validated_data.pop('quantity')
        price_per_unit = validated_data.pop('price_per_unit')
        batch_number = validated_data.pop('batch_number')
        unit = validated_data.pop('unit', 'kg')

        #unit minimum enforcement
        if unit in ['kg', 'litre'] and quantity < 30:
            raise serializers.ValidationError(f'Quantity must be at least 30 {unit}')
        if unit in ['unit'] and quantity < 1:
            raise serializers.ValidationError(f'Quantity must be at least 1')

        
        #accept input by name not fk id
        category_name  = self.initial_data.get('category')


        if category_name:
            category_object,_ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category_object

        validated_data['farmer'] = user

        produce = super().create(validated_data)

        ProduceBatch.objects.create(
            produce=produce,
            quantity = quantity,
            unit = unit,
            price_per_unit=price_per_unit,
            batch_number = batch_number,
            harvest_date = timezone.now().date()
        )
        return produce