from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Service
from .serializers import ServiceSerializer
from .permissions import IsFieldOfficer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
class ServiceViewset(viewsets.ModelViewSet):
    #queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsFieldOfficer]

    def get_queryset(self):
        user = self.request.user
        #only farmers and field officers can view
        if self.request.user.role == 'buyer':
            return Service.objects.none()
        else:
            get_all = Service.objects.filter(provider=user)
            
        return get_all
    
    #save the created service
    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)
