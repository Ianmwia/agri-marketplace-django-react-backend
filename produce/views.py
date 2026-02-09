from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import Produce
from .serializers import ProduceSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from orders.models import Order

# Create your views here.

class IsAFarmer(permissions.BasePermission):
    '''check if the authenticated user role is farmer'''
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'
    
class ProduceViewSet(viewsets.ModelViewSet):
    serializer_class = ProduceSerializer
    permission_classes = [IsAFarmer]

    #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'produce.html'

    def list(self, request, *args, **kwargs):
        # get the farmers produce
        serializer = self.get_serializer()
        orders = Order.objects.filter(produce__farmer=request.user)
        return Response({'serializer': serializer, 'orders': orders})

    def get_queryset(self):
        '''list all each farmers produce'''
        #swagger line for mock anon user to 
        if getattr(self, 'swagger_fake_view', False):
            return Produce.objects.none()
        
        return Produce.objects.filter(farmer=self.request.user).order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    