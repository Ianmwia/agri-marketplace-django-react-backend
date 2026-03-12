from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Logistics
from .serializers import LogisticsSerializer


# Create your views here.
class LogisticsViewset(viewsets.ModelViewSet):
    serializer_class = LogisticsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Logistics.objects.select_related(
            'order__batch__produce__farmer'
        )