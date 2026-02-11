from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['reported_by', 'title', 'description', 'assigned_to']
        read_only_fields = ['reported_by', 'created_at']