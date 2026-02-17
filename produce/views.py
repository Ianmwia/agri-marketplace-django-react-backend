from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions, serializers
from .models import Produce
from .serializers import ProduceSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from orders.models import Order
from reports.serializers import ReportSerializer
from rest_framework.decorators import action
from accounts.models import CustomUser
from reports.models import Report

# Create your views here.

class IsAFarmer(permissions.BasePermission):
    '''check if the authenticated user role is farmer'''
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'
    
class ProduceViewSet(viewsets.ModelViewSet):
    serializer_class = ProduceSerializer
    permission_classes = [IsAFarmer]

    #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'produce.html'

    def list(self, request, *args, **kwargs):
        # get the farmers produce
        serializer = self.get_serializer()
        orders = Order.objects.filter(produce__farmer=request.user)
        produce_list = self.get_queryset()

        reports = Report.objects.filter(reported_by=request.user).order_by('-created_at')
        report_serializer = ReportSerializer()
        report_serializer.fields['assigned_to'].queryset = CustomUser.objects.filter(role='agrivet')
        return Response({'serializer': serializer, 'orders': orders, 'produce_list':produce_list, 'report_serializer':report_serializer, 'reports': reports})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return self.list(request, *args, **kwargs)
        
        orders = Order.objects.filter(produce__farmer=request.user)
        report_serializer = ReportSerializer()

        return Response({'serializer': serializer, 'orders': orders, 'report_serializer': report_serializer})
    
    @action(detail=False, methods=['post'])
    def submit_report(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reported_by=request.user)
        return redirect('produce-list')

    def get_queryset(self):
        '''list all each farmers produce'''
        #swagger line for mock anon user to 
        if getattr(self, 'swagger_fake_view', False):
            return Produce.objects.none()
        
        return Produce.objects.filter(farmer=self.request.user).order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    