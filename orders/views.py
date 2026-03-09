from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, ProduceBatchSerializer
from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from produce.models import Produce, ProduceBatch
from produce.serializers import ProduceSerializer
from rest_framework.permissions import BasePermission
from django.db.models import F

#mpesa
from mpesa.views import initialize_stk_push
from mpesa.models import MpesaRequest, MpesaResponse

#textbee sms
from accounts.helpers import send_free_sms, normalize_phone_number


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'buyer' or request.user.role == 'farmer'


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    '''
    Buyer creates orders
    Buyer views their own orders
    Farmer views orders on their produce
    '''
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]

    #http render in django
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        
        user = self.request.user
        if user.role == 'buyer':
            return Order.objects.filter(buyer=user).select_related('batch__produce')
        
        if user.role == 'farmer':
            return Order.objects.filter(batch__produce__farmer=user).select_related('batch__produce')
        
        

        return Order.objects.none()

    def list(self, request, *args, **kwargs):
        #get empty serializer
        serializer = self.get_serializer()
        
        #get existing orders
        orders = self.get_queryset()

        #get available produce so a buyer can select an item
        available_batches = ProduceBatch.objects.filter(quantity__gt=0).select_related('produce')
        #serialized_batches = ProduceBatchSerializer(available_batches, many=True)

        #search feature
        search_query = request.query_params.get('q', '')

        #apply filters
        if search_query:
            #search by produce name
            available_batches = available_batches.filter(produce__name__icontains=search_query)

        if request.accepted_renderer.format == 'json':
            return Response({
                'orders': OrderSerializer(orders, many=True).data,
                'available_batches':  ProduceBatchSerializer(available_batches, many=True).data,
            })

        return Response({'serializer': serializer.data, 
                         'orders': orders,
                         'available_produce': available_batches})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        
            orders = self.get_queryset()
            available_produce = ProduceBatch.objects.filter(quantity__gt=0)
            return Response({
                'serializer': serializer.data,
                'orders':OrderSerializer(orders, many=True).data, 
                'available_produce': ProduceBatchSerializer(available_produce, many=True).data})
        #orders = self.get_queryset()
        #available_produce = ProduceBatch.objects.filter(quantity__gt=0)
        return Response({
            "error": serializer.errors
        })
    
    # def get_queryset(self):
    #     #swagger line for mock anon user to 
    #     if getattr(self, 'swagger_fake_view', False):
    #         return Order.objects.none()
        
    #     user = self.request.user
    #     if user.role == 'buyer':
    #         return Order.objects.filter(buyer=user)
        
    #     if user.role == 'farmer':
    #         return Order.objects.filter(produce__farmer=user)
        
    #     return Order.objects.none()
    
# farmers accept or reject orders
# use actions since viewsets provide crud not accept or reject , these are custom
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        '''
        Farmer accepts an order
        '''
        order = self.get_object()

        if request.user != order.batch.produce.farmer:
            return Response(
                {'error': 'You are not allowed to accept this order'}
            )
        
        order.status = 'accepted'
        order.save()

        #send sms message from text bee to buyer that order is accepted
        msg = f'Order Confirmed: The farmer has accepted your request, please proceed to pay'
        send_free_sms(order.buyer.phone, msg)

        return Response({"message": "Order Accepted and SMS sent", 'status': order.status})
    
    #mpesa pay after accept
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object()

        if order.status != 'accepted':
            return Response({'error': 'Order must be accepted first'})
        
        #mpesa request object
        mpesa_req = MpesaRequest.objects.create(
            order=order,
            phone_number = request.user.phone,
            amount = order.total_price,
            account_reference=f'ORDER {order.id}',
            transaction_description = f'Payment for {order.batch.produce.name}',
        )
        #call init logic
        response_data = initialize_stk_push(mpesa_req)

        #handle response
        if response_data.get('ResponseCode') == '0':
            MpesaResponse.objects.create(
                request = mpesa_req,
                merchant_request_id = response_data.get('MerchantRequestID'),
                checkout_request_id = response_data.get('CheckoutRequestID'),
                response_code = response_data.get('ResponseCode'),
                customer_message = response_data.get('CustomerMessage'),
            )

        #update order
            order.mpesa_checkout_id = response_data.get('CheckoutRequestID')
            order.save()
            return Response(response_data)
        
        return Response({'Error': "Safaricom rejected the request"})

    

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        '''
        Farmer rejects an order
        '''
        order = self.get_object()

        if request.user != order.batch.produce.farmer:
            return Response(
                {'error': 'You are not allowed to accept this order'}
            )
        
        # if rejected
        if order.status == 'rejected':
            return Response({"message": "Order is already rejected"})
        
            #give the farmer back the stock
        batch = order.batch
        batch.quantity += order.quantity
        batch.save()

            #get rejection reason and update order 
        reason = request.data.get("reason") or request.data.get("rejection_reason") or 'No Reason Provided'
        order.status = 'rejected'
        order.rejection_reason = reason
        order.save()

            #send sms message from text bee to buyer that order is rejected
        msg = f'Order Rejected: The farmer has rejected your request, please check your orders list to see the reason why'
        send_free_sms(order.buyer.phone, msg)

        return Response({'message': 'Order already rejected', 'reason': reason})
    

    @action(detail=True, methods=['post'])
    def delivered(self, request, pk=None):
        '''
        Only accepted orders can be delivered
        '''
        order = self.get_object()

        if request.user != order.batch.produce.farmer:
            return Response(
                {'error': 'You are not allowed to mark this order as delivered'}
            )
        
        if order.status != 'accepted':
            return Response(
                {'error': 'Only accepted Orders can be delivered'}
            )
        
        order.status = 'delivered'
        order.save()
        return Response({"message": "Order Delivered"})
    
    
