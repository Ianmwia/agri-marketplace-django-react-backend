from rest_framework import serializers
from .models import Category, Produce

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != 'farmer':
            raise serializers.ValidationError('only farmers can create produce')
        validated_data['farmer'] = user
        return super().create(validated_data)