from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import Produce
from .serializers import ProduceSerializer

# Create your views here.

class IsAFarmer(permissions.BasePermission):
    '''check if the authenticated user role is farmer'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'
    
class ProduceViewSet(viewsets.ModelViewSet):
    serializer_class = ProduceSerializer
    permission_classes = [IsAFarmer]

    def get_queryset(self):
        '''list all each farmers produce'''
        return Produce.objects.filter(farmer=self.request.user).order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    