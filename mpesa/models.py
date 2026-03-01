from django.db import models

# Create your models here.
# we create 2 models
#request body
class MpesaRequest(models.Model):
    phone_number = models.CharField( max_length=16)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_reference = models.CharField(max_length=50)
    transaction_description = models.CharField(max_length=255)
    timestamp =models.DateTimeField(auto_now_add=True)

#response body
class MpesaResponse(models.Model):
    request = models.ForeignKey(MpesaRequest, on_delete=models.CASCADE, related_name='responses')
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255)
    response_code = models.CharField(max_length=10)
    response_description = models.CharField(max_length=255)
    customer_message = models.CharField(max_length=255)
    timestamp =models.DateTimeField(auto_now_add=True)

