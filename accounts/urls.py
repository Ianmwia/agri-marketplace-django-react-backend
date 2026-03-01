from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet, LogoutView, UpdateProfileView, MeView
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
    path('me/', MeView.as_view(), name ='me'),

    path('user-choices',views.user_choices, name='user-choices'),  
    path('users/',views.get_users, name='get-users'),  
    path('csrf/',views.get_csrf, name='csrf'),   
    path('', include(router.urls)),
     
]
