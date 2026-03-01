from django.shortcuts import render
from .serializers import ThreadSerializer, MessageSerializer
from .models import Thread, Message
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Thread.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).select_related('user1', 'user2')
    
    def create(self, request, *args, **kwargs):
        user1 = request.user
        user2_id = request.data.get('user2')

        if not user2_id:
            return Response({'Error': "User2 ID is required"})#400
        
        try:
            user2 =User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"})
    
        if user1 == user2:
            return Response({"Error": "You cannot chat with yourself"})
        
        u1, u2 = (user1, user2) if user1.id < user2.id else (user2, user1)

        thread, created = Thread.objects.get_or_create(user1=u1, user2=u2)

        serializer = self.get_serializer(thread)
        return Response(serializer.data)#201


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Message.objects.filter(
            Q(thread__user1=user) | Q(thread__user2=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)