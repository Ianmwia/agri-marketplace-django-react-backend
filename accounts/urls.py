from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet, LogoutView, UpdateProfileView
from django.urls import path, include
from . import views

router = DefaultRouter()
#router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = [
    path('',views.landing, name='landing'),

    path('register/', RegisterViewSet.as_view(), name ='register'),
    path('profile/', UpdateProfileView.as_view(), name ='profile'),
    path('logout/', LogoutView.as_view(), name ='logout'),

    path('user-choices',views.user_choices, name='user-choices'),
    
    path('', include(router.urls)),
     
]
