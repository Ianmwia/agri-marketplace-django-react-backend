from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls))
]
