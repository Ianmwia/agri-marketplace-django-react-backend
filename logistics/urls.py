from rest_framework.routers import DefaultRouter
from .views import LogisticsViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'logistics', LogisticsViewset, basename='logistics')

urlpatterns = router.urls
