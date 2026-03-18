from django.shortcuts import render
from .serializers import ThreadSerializer, MessageSerializer
from .models import Thread, Message
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()

# Create your views here.
class ThreadViewSet(viewsets.ModelViewSet):
    '''viewset for managing conversations
    -Buyer & farmer
    -Farmer * field officer 
    '''

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # return Thread.objects.filter(
        #     Q(user1=user) | Q(user2=user)
        # ).select_related('user1', 'user2', 'order__batch__produce').order_by('-updated_at') 

        if user.role == 'buyer':
            #buyer can only chat to farmers they placed order with
            farmer_ids = Order.objects.filter(buyer=user)\
                .values_list('batch__produce__farmer_id', flat=True).distinct()
            return User.objects.filter(id__in=farmer_ids)
        
        elif user.role == 'farmer':
            #farmer can only chat to buyers who placed an order
            buyer_ids = Order.objects.filter(buyer=user)\
                .values_list('buyer_id', flat=True).distinct()
            return User.objects.filter(id__in=buyer_ids)
        
        elif user.role == 'field_officer':
            #field officer only chat to farmers
            return User.objects.filter(role='farmer')
        
        return User.objects.none()
        
    
    def create(self, request, *args, **kwargs):
        user1 = request.user
        user2_id = request.data.get('user2')
        order_id = request.data.get('order')

        if not user2_id:
            return Response({'Error': "User2 ID is required"})#400
        
        try:
            user2 =User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"})
    
        if user1 == user2:
            return Response({"Error": "You cannot chat with yourself"})
        
        #prevent buyer and field officer
        roles = {user1.role, user2.role}
        if 'buyer' in roles and 'field_officer' in roles:
            return Response({
                'error':'Communication between Buyer and Field Officer not permitted'
            })
        
        #buyer -> farmer only allowed if an order is placed
        if 'buyer' in roles and 'farmer' in roles:
            order_exists = Order.objects.filter(
                buyer=user1 if user1.role == 'buyer' else user2,
                batch__produce__farmer=user2 if user2.role == 'farmer' else user1
            ).exists()

            if not order_exists:
                return Response({
                    'error':'You can only chat with a farmer after placing an order with said farmer'
                })
        
        #maintain unique IDs
        u1, u2 = (user1, user2) if user1.id < user2.id else (user2, user1)

        thread, created = Thread.objects.get_or_create(user1=u1, user2=u2)

        if order_id:
            try:
                order_obj = Order.objects.get(id=order_id)
                thread.order = order_obj
                thread.save()
            except Order.DoesNotExist:
                pass

        serializer = self.get_serializer(thread)
        return Response(serializer.data)#201


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Message.objects.filter(
            Q(thread__user1=user) | Q(thread__user2=user)
        ).order_by('created_at')

        thread_id = self.request.query_params.get('thread')
        if thread_id:
            queryset = queryset.filter(thread_id=thread_id)
            return queryset

    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)