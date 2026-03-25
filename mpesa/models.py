from django.db import models
from orders.models import Order

# Create your models here.
# we create 2 models
#request body
class MpesaRequest(models.Model):
    order = models.ForeignKey(Order, related_name='mpesa_requests', on_delete=models.CASCADE)
    phone_number = models.CharField( max_length=16)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_reference = models.CharField(max_length=50)
    transaction_description = models.CharField(max_length=255)
    timestamp =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request for order  {self.order.id} - {self.amount}'

#response body
class MpesaResponse(models.Model):
    request = models.ForeignKey(MpesaRequest, on_delete=models.CASCADE, related_name='responses')
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255, unique=True)
    response_code = models.CharField(max_length=10)
    response_description = models.CharField(max_length=255)
    customer_message = models.CharField(max_length=255)
    timestamp =models.DateTimeField(auto_now_add=True)

class MpesaCallBack(models.Model):
    checkout_request_id = models.CharField(max_length=50)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=255)

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mpesa_receipt_number = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Callback {self.checkout_request_id} - Result: {self.result_code}'

#STRIPE
class StripePayment(models.Model):
    order = models.ForeignKey(Order, related_name='stripe_pay', on_delete=models.CASCADE)

    stripe_checkout_id= models.CharField(max_length=50, unique=True)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50, default='kes')

    #stripe webhook status
    status = models.CharField(max_length=50, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)