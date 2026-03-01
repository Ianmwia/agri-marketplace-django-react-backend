from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Thread(models.Model):
    ''' Container for thread, so keep 2 users in conversation'''
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads_user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads_user2')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user1', 'user2'],
                name='unique_thread'
            )
        ]

    def clean(self):
        #prevent self messaging
        if self.user1 == self.user2:
            raise ValidationError('Users cannot message themselves')
        
        #ensure user1 and user2 prevent duplicate containers
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.user1_id > self.user2_id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user1.role} & {self.user2.role} Chat'
    
class Message(models.Model):
    thread = models.ForeignKey(Thread ,on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']