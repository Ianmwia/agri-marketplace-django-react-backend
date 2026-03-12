from django.db import models
from orders.models import Order

# Create your models here.
class Logistics(models.Model):
    STATUS = (
        ('scheduled','Scheduled'),
        ('in_transit','In Transit'),
        ('delivered','Delivered'),
        ('failed', 'Failed')
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    status = models.CharField(max_length=50, choices=STATUS, default='scheduled')
    dropoff_lat = models.FloatField()
    dropoff_lon = models.FloatField()