from rest_framework import serializers
from .models import Logistics

class LogisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Logistics
        fields = '__all__'
        read_only_fields = ['status']