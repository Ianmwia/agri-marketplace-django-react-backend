from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, ProduceBatchSerializer
from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from produce.models import Produce, ProduceBatch
from produce.serializers import ProduceSerializer
from rest_framework.permissions import BasePermission
from django.db.models import F, Q

#mpesa
from mpesa.views import initialize_stk_push
from mpesa.models import MpesaRequest, MpesaResponse

#textbee sms
from accounts.helpers import send_free_sms, normalize_phone_number

#pagination
from .pagination import Pagination, MarketPlacePagination

#ordering
from rest_framework.filters import OrderingFilter

# csv
import csv
from django.http import HttpResponse
from django.utils import timezone

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
    pagination_class = Pagination

    #http render in django
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        
        user = self.request.user

        queryset = Order.objects.select_related(
            "buyer",
            "batch__produce",
            "batch__produce__farmer",
            "delivery"
        ).exclude(status='canceled')
        
        if user.role == 'buyer':
            return queryset.filter(buyer=user).order_by('-created_at')
        
        if user.role == 'farmer':
            return queryset.filter(batch__produce__farmer=user).order_by('-created_at')
        
        

        return Order.objects.none()
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        user = request.user
        name = f'{user.first_name} {user.last_name}'.strip()
        role = user.role

        clean_name = name.replace(' ', '_')

        date_str = timezone.now().strftime('%Y-%m-%d_%H:%M')
        filename = f'{role}_{clean_name}_Orders_{date_str}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        # writer.writerow(['Order ID', 'Produce', 'Farmer', 'Quantity', 'Unit', 'Total Price', 'Status', 'Date'])
        if role == 'buyer':
            writer.writerow(['Order ID', 'Produce', 'Farmer', 'Quantity', 'Unit', 'Total Price', 'Status', 'Date'])
                    
        elif role == 'farmer':
            writer.writerow(['Order ID', 'Produce', 'Buyer', 'Quantity', 'Unit','Phone', 'Total Price', 'Status', 'Date'])


        orders = self.get_queryset()

        for order in orders:
            # writer.writerow([
            #     order.id,
            #     order.batch.produce.name,
            #     f"{order.batch.produce.farmer.first_name} {order.batch.produce.farmer.last_name}",
            #     order.quantity,
            #     order.batch.unit,
            #     order.total_price,
            #     order.status,
            #     order.created_at.strftime('%Y-%m-%d %H-%M'),
            # ])
            if role == 'buyer':
               writer.writerow([
                order.id,
                order.batch.produce.name,
                f"{order.batch.produce.farmer.first_name} {order.batch.produce.farmer.last_name}",
                order.quantity,
                order.batch.unit,
                order.total_price,
                order.status,
                order.created_at.strftime('%Y-%m-%d %H:%M'),
            ]) 
            elif role == 'farmer':
                writer.writerow([
                order.id,
                order.batch.produce.name,
                f"{order.buyer.first_name} {order.buyer.last_name}",
                order.quantity,
                order.batch.unit,
                f"'{order.buyer.phone}",
                order.total_price,
                order.status,
                order.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        return response


    def list(self, request, *args, **kwargs):
        #get empty serializer
        serializer = self.get_serializer()
        
        #get existing orders
        orders = self.get_queryset()

        #get available produce so a buyer can select an item
        available_batches = ProduceBatch.objects.filter(
            quantity__gt=0).select_related('produce', 'produce__farmer')
        #serialized_batches = ProduceBatchSerializer(available_batches, many=True)

        #search feature
        search_query = request.query_params.get('q', '')

        #apply filters
        if search_query:
            #search by produce name
            available_batches = available_batches.filter(
                Q(produce__name__icontains=search_query) | Q(produce__farmer__location__icontains=search_query))
            
        marketplace_paginator = MarketPlacePagination()
        marketplace_page = marketplace_paginator.paginate_queryset(available_batches, request)
            
        #pagination
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            
            if request.accepted_renderer.format == 'json':
                response = self.get_paginated_response(serializer.data)

                response.data['orders'] = serializer.data
                response.data['available_batches'] = ProduceBatchSerializer(marketplace_page, many=True).data
                return response
        return Response({
            'serializer': serializer.data,
            'orders': serializer.data,
            'available_produce': ProduceBatchSerializer(available_batches, many=True).data
        })

                #fallback from pagination
        serializer = self.get_serializer(orders, many=True)
        return Response({'serializer': serializer.data, 
                         'orders': orders,
                         'available_produce': available_batches})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        
            orders = self.get_queryset()
            available_produce = ProduceBatch.objects.filter(quantity__gt=0).select_related('produce', 'produce__farmer')[:25]
            return Response({
                'message': 'Order placed successfully',
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
    
    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        user = request.user

        if user != order.buyer:
            return Response ({'error': 'Only the buyer can cancel an order'})
        
        #cant cancel if order is delivered
        if order.status == ['delivered', 'canceled']:
            return Response ({'error': 'Delivered orders cannot be canceled'})
        if order.status == 'canceled':
            return Response ({'error': 'Order is already canceled'})
        # restore stock if cancelled
        
        batch = order.batch
        batch.quantity = F('quantity') + order.quantity
        batch.save(update_fields=['quantity'])

        batch.refresh_from_db(fields=['quantity'])

        order.status = 'canceled'
        order.save(update_fields=['status'])

        #auto refresh frontend
        orders_queryset = self.get_queryset()

        page = self.paginate_queryset(orders_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            available_batches = ProduceBatch.objects.filter(quantity__gt=0).select_related('produce', 'produce__farmer')
            response.data['orders'] =serializer.data
            response.data['available_produce'] = ProduceBatchSerializer(available_batches, many=True).data
            return response
        
        #pagination fallback
        return Response ({
            'message': 'Order canceled',
            'status': order.status,
            'orders': OrderSerializer(orders_queryset, many=True).data,
            'available_produce': ProduceBatchSerializer(available_batches, many=True).data
        })
    
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
    
    
