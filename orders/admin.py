from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'produce', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['buyer__email', 'produce__name']
    
admin.site.register(Order, OrderAdmin)