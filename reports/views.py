from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


    #http render in django
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reports.html'

    def get(self, request):
        queryset = self.get_queryset()
        return Response({'reports': queryset})
    