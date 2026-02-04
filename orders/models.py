from django.db import models
from django.conf import settings
from produce.models import Produce
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Order(models.Model):
    """
    order model
    -buyer places order for a produce
    -farmer accepts or rejects
    """
    STATUS = (
        ('pending','Pending')
        ('accepted','Accepted')
        ('rejected','Rejected')
        ('delivered','Delivered')
    )
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(_("number of items ordered"))
    status = models.CharField(_("purchase status"), max_length=50, choices=STATUS, default='pending')
    created_at = models.DateTimeField(_("date when produce was ordered"), auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.produce.name}'