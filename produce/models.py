from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator


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
    
    def __str__(self):
        return f'{self.name} by {self.farmer.email}'
    
class ProduceBatch(models.Model):
    produce = models.ForeignKey(Produce, related_name='batches', on_delete=models.CASCADE)
    batch_number = models.CharField(unique=True, max_length=20)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(10)],
        help_text=('Enter quantity above 10kgs')
    )
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2,
            validators=[MinValueValidator(400)],
            help_text=('Minimum price per quantity is Kes 400'))
    harvest_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.produce.name} - {self.batch_number} ({self.quantity} left)'