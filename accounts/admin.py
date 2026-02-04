from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customuser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = Customuser
    list_display = ['email', 'first_name', 'last_name']
    search_fields = ['email']
    ordering = ('email',)
admin.site.register(Customuser, CustomUserAdmin)