from rest_framework import serializers
from .models import Category, Produce
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProduceSerializer(serializers.ModelSerializer):
    #accept input by email not fk id
    image = serializers.ImageField(required=False, allow_null=True)

    farmer = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        required = False
    )

    category = serializers.CharField()
    class Meta:
        model = Produce
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != 'farmer':
            raise serializers.ValidationError('only farmers can create produce')
        
        #accept input by name not fk id
        category_name  = self.initial_data.get('category')

        if category_name:
            category_object,_ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category_object

        validated_data['farmer'] = user
        return super().create(validated_data)