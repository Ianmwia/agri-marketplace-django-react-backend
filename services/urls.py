from rest_framework.routers import DefaultRouter
from .views import ServiceViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'service', ServiceViewset, basename='service')

urlpatterns = [
    path('', include(router.urls))
]
