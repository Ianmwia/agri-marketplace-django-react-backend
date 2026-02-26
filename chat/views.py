from django.shortcuts import render
from .serializers import ThreadSerializer, MessageSerializer
from .models import Thread, Message
from rest_framework import viewsets, permissions
from django.db.models import Q

# Create your views here.
class ThreadViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Thread.objects.filter(
            Q(user1=user) | Q(user2=user)
        )
    
    def perform_create(self, serializer):
        serializer.save()


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