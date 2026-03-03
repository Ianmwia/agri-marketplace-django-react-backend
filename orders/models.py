from django.db import models
from django.conf import settings
from produce.models import Produce, ProduceBatch
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Order(models.Model):
    """
    order model
    -buyer places order for a produce
    -farmer accepts or rejects
    """
    STATUS = (
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
        ('paid', 'Paid'),
        ('delivered','Delivered')
    )
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_orders')
    batch = models.ForeignKey(ProduceBatch, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("number of items ordered"))
    status = models.CharField(_("purchase status"), max_length=50, choices=STATUS, default='pending')

    #mpesa financials
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    mpesa_checkout_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(_("date when produce was ordered"), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #add rejection reason
    rejection_reason = models.TextField(_("reason for rejection"), blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.batch.price_per_unit * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.id} - {self.batch.produce.name}'