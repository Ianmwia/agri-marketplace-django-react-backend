from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Report(models.Model):
    '''
    Report for disease outbreaks or farm issues
    '''
    STATUS = (
        ('reported','Reported'),
        ('ongoing','Ongoing'),
        ('resolved','Resolved')
    )
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='report')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(_(""), max_length=50)
    description = models.TextField(_(""))
    status = models.CharField(_("issue report status"), max_length=50, choices=STATUS, default='reported')

    def __str__(self):
        return self.title


