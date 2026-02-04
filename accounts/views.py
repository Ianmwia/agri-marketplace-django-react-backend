from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import viewsets

from django.contrib.auth import authenticate

# Create your views here.
#class based Api Views
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    
class LoginViewSet(viewsets.ViewSet):
    '''
    LoginViewSet
    ViewSet  - to check for valid credentials vs ModelViewSet used for crud
    create must be implemented
    return error if credentials are invalid
    return 405 
    '''
    serializer = LoginSerializer
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            #authenticate against django auth system
            user = authenticate(request, email=email, password=password)
            if user:
                return Response({
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'location': user.location,
                })
            return Response({'error': "Invalid email or password"})

        return Response(serializer.errors)