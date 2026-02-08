from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from cloudinary.models import CloudinaryField


# Create your models here.
class Category(models.Model):
    name = models.CharField(_("categories"), max_length=100, unique=True)
    def __str__(self):
        return self.name
    
class Produce(models.Model):
    '''
    creates a many to one relationship, many produce to one farmer
    '''
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("associated farmer"), on_delete=models.CASCADE)
    name = models.CharField(_("name of produce"), max_length=100)
    #if category is deleted set it to null instead of deleting the produce
    category = models.ForeignKey(Category, verbose_name=_("produce category"), on_delete=models.SET_NULL, null=True)
    image = CloudinaryField("product image", blank=True)
    description = models.TextField(_("produce description"))
    quantity = models.PositiveIntegerField(_("amount of produce"))
    price = models.DecimalField(_("price of produce"), max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} by {self.farmer.first_name} {self.farmer.email}'