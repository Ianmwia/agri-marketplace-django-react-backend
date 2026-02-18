from django.db import models
from accounts.models import CustomUser
from django.conf import settings

# Create your models here.
class Service(models.Model):
    '''
    B2B professional marketplace, to allow farmers to book services not just contact them
    farmers request contacts
    -field office is assigned and offers the service with charge

    '''
    SERVICE_CHOICES = {
        #Animal
        ('veterinarian', 'Veterinarian'),
        ('livestock_showman', 'Livestock Showman'),
        #Soil
        ('soil_technician', 'Soil Technician'),
        #Machinery
        ('tractor_service', 'Tractors'),
    }

    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offered_services')
    title = models.CharField(choices=SERVICE_CHOICES) # title of the field officer , the sub role
    category = models.CharField(max_length=50, choices=CustomUser.FIELDS)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #allow farmers to search by specialty
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.provider.first_name}"