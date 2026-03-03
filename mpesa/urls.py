from django.urls import path
from mpesa.views import *

urlpatterns = [
    path('api/stk_push/', stk_push, name='stk-push')
]
