from django.urls import path
from mpesa.views import *
from mpesa.views import stripe_checkout, stripe_webhook

urlpatterns = [
    path('api/stk_push/', stk_push, name='stk-push'),
    #stripe
    path('stripe/pay/', stripe_checkout, name='stripe_pay'),
    path('stripe/webhook', stripe_webhook, name='stripe_webhook')
]
