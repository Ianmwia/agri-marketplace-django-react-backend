from django.shortcuts import render
from rest_framework import viewsets
from .models import Produce
from .serializers import ProduceSerializer

# Create your views here.
class ProduceViewSet(viewsets.ModelViewSet):
    queryset = Produce.objects.all().order_by('-date_created')
    serializer_class = ProduceSerializer