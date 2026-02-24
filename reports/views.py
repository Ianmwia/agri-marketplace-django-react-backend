from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    #queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


    #http render in django
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'reports.html'

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'role') and user.role == 'field_officer':
            return Report.objects.filter(assigned_to=self.request.user).order_by('-created_at')
        
        return Report.objects.filter(reported_by=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        #serializer = self.get_serializer(queryset, many=True)
        return Response({'reports': queryset})
    