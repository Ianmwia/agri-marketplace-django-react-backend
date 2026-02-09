from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, ProfileUpdateSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
#class based Api Views
class RegisterViewSet(APIView):
    permission_classes = []
    serializer_class = RegisterSerializer 
    #only post no get

    #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'

    def get(self, request):
        serializer = RegisterSerializer
        return Response({'serializer': serializer})
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration Successful', 'serializer': serializer})
        return Response({'serializer': serializer, 'errors': serializer.errors})
    
class LoginViewSet(viewsets.ViewSet):
    '''
    LoginViewSet
    ViewSet  - to check for valid credentials vs ModelViewSet used for crud
    create must be implemented
    return error if credentials are invalid
    return 405 
    '''
    serializer_class = LoginSerializer

     #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        serializer = LoginSerializer
        return Response({'serializer': serializer})

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

            return redirect('profile')
            
            # return Response({
            #     'id': user.id,
            #     'message': 'Login Successful',
            #     'role': user.role,
            #     'email': user.email,
            # })
        return Response({ 'serializer': serializer, 'errors' :serializer})
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'logout.html'

    def get(self, request):
        return Response({})

    def post(self, request):
        logout(request)
        return redirect('login-list')
        #return Response({'message': "Successfully Logged Out"})
    
class UpdateProfileView(APIView):
    '''
    get a users profile and update

    '''    
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile.html'

    def get(self, request):
        '''
        get the existing users data
        '''
        user = request.user
        serializer = ProfileUpdateSerializer(user)

        #edit mode for template rendering a single users profile
        edit_mode = request.GET.get('edit') == '1'

        return Response({'data':serializer, 'serializer': serializer, 'edit_mode': edit_mode})
    
    def post(self, request):
        '''
        use put to update the data / use post for browser
        request the users data
        and partial to update just one field at a time
        '''
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response({'message': 'Profile updated', 'serializer': serializer})
        
        return Response(serializer.errors)
