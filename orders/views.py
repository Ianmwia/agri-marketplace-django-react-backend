from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    '''
    Buyer creates orders
    Buyer views their own orders
    Farmer views orders on their produce
    '''
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'buyer':
            return Order.objects.filter(buyer=user)
        
        if user.role == 'farmer':
            return Order.objects.filter(produce__farmer=user)
        
        return Order.objects.none()