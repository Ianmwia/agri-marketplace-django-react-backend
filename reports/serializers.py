from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, min_length=2)
    description = serializers.CharField(required=True)

    farmer_name = serializers.ReadOnlyField(source='reported_by.first_name')
    farmer_email = serializers.ReadOnlyField(source='reported_by.email')
    class Meta:
        model = Report
        fields = ['reported_by', 'title', 'description', 'assigned_to', 'status', 'created_at', 'farmer_name', 'farmer_email']
        read_only_fields = ['reported_by', 'created_at']