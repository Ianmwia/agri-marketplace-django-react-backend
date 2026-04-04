from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_password_reset_url(self, request, user):
        return f'{settings.FRONTEND_URL}/reset-password/'
