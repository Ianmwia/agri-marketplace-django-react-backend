from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, ProfileUpdateSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout

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

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            #authenticate against django auth system
            user = authenticate(request, email=email, password=password)
            if not user:
                return Response({'error': "Invalid email or password"})
            
            login(request, user)
            
            return Response({
                'id': user.id,
                'message': 'Login Successful',
                'role': user.role,
                'email': user.email,
            })
        return Response(serializer.errors)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': "Successfully Logged Out"})
    
class UpdateProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileUpdateSerializer