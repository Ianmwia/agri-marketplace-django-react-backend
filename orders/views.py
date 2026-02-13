from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from produce.models import Produce


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    '''
    Buyer creates orders
    Buyer views their own orders
    Farmer views orders on their produce
    '''
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order.html'

    def list(self, request, *args, **kwargs):
        #get empty serializer
        serializer = self.get_serializer()
        
        #get existing orders
        orders = self.get_queryset()

        #get available produce so a buyer can select an item
        available_produce = Produce.objects.filter(quantity__gt=0)

        return Response({'serializer': serializer, 'orders':orders, 'available_produce': available_produce})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return redirect('order-list')
        
        orders = self.get_queryset()
        available_produce = Produce.objects.all()
        return Response({
            'serializer': serializer,
            'orders':orders,
            'available_produce': available_produce
        })
    
    def get_queryset(self):
        #swagger line for mock anon user to 
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        
        user = self.request.user
        if user.role == 'buyer':
            return Order.objects.filter(buyer=user)
        
        if user.role == 'farmer':
            return Order.objects.filter(produce__farmer=user)
        
        return Order.objects.none()
    
# farmers accept or reject orders
# use actions since viewsets provide crud not accept or reject , these are custom
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        '''
        Farmer accepts an order
        '''
        order = self.get_object()

        if request.user != order.produce.farmer:
            return Response(
                {'error': 'You are not allowed to accept this order'}
            )
        
        order.status = 'accepted'
        order.save()
        return Response({"message": "Order Accepted"})
    

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        '''
        Farmer rejects an order
        '''
        order = self.get_object()

        if request.user != order.produce.farmer:
            return Response(
                {'error': 'You are not allowed to accept this order'}
            )
        
        # get reason form
        reason = request.data.get("rejection_reason", "No reason provided")
        
        # delete the order
        order.delete()
        
        #return Response({"message": "Order Rejected", 'reason':reason})
        return redirect('produce-list')
    

    @action(detail=True, methods=['post'])
    def delivered(self, request, pk=None):
        '''
        Only accepted orders can be delivered
        '''
        order = self.get_object()

        if request.user != order.produce.farmer:
            return Response(
                {'error': 'You are not allowed to accept this order'}
            )
        
        if order.status != 'accepted':
            return Response(
                {'error': 'Only accepted Orders can be delivered'}
            )
        
        order.status = 'delivered'
        order.save()
        return Response({"message": "Order Delivered"})
    
    
