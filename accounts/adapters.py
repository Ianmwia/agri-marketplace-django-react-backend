from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_password_reset_url(self, request, user):
        return f'{settings.FRONTEND_URL}/reset-password/'


from dj_rest_auth.serializers import PasswordResetSerializer
class CustomPasswordSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            'extra_email_context':{
                'password_reset_url' : f'{settings.FRONTEND_URL}/reset-password/'
            }
        }
        
