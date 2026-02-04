from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls))
]
