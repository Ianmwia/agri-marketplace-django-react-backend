from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Produce

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name')
    search_fields = ('name',)
   
admin.site.register(Category, CategoryAdmin)

class ProduceAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name', 'farmer', 'category', 'quantity', 'price' , 'date_created')
    search_fields = ('name', 'farmer__name',)
    
admin.site.register(Produce, ProduceAdmin)