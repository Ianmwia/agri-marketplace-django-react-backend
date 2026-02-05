from django.contrib import admin
from .models import Report

# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reported_by', 'created_at', 'title', 'description']
    list_filter = ['created_at']
    search_fields = ['status']
    
admin.site.register(Report, ReportAdmin)