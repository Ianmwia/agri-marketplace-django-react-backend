from django.contrib import admin
from .models import MpesaCallBack, MpesaRequest, MpesaResponse, StripePayment

# Register your models here.
admin.site.register(MpesaCallBack)
admin.site.register(MpesaResponse)
admin.site.register(MpesaRequest)
admin.site.register(StripePayment)
