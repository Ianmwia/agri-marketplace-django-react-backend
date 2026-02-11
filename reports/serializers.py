from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, min_length=2)
    description = serializers.CharField(required=True)
    class Meta:
        model = Report
        fields = ['reported_by', 'title', 'description', 'assigned_to']
        read_only_fields = ['reported_by', 'created_at']