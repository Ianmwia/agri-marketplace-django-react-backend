from rest_framework.routers import DefaultRouter
from .views import ProduceViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'produce', ProduceViewSet, basename='produce')

urlpatterns = [
    path('', include(router.urls))
]
