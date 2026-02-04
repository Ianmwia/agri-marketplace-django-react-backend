from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ('email',)

    #field shown when editing an existing user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Info', {'fields': ('first_name', 'last_name', 'role', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    #field shown when creating a new user
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email','password1', 'password2','first_name', 'last_name', 
                           'role', 'location',
                           'is_active', 'is_staff', 'is_superuser'
                        ),
                }),
        )


admin.site.register(CustomUser, CustomUserAdmin)