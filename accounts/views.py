from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import viewsets

# Create your views here.
#class based Api Views
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    
class LoginViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    