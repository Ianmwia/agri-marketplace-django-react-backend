from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet, LogoutView, UpdateProfileViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'profile', UpdateProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name ='logout' )
]
