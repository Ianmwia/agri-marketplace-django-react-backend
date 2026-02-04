from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):
    '''
    Creating users with CustomUserManager, using AbstractBaseUser for full control
    compared to django user model and slightly altered AbstractUser
    Create UseManager as its not given by django 
    '''
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
    Customuser to extend baseUser manager for authentication and permissions
    '''
    ROLES = (
        ('farmer', 'Farmer'),
        ('buyer','Buyer'),
        ('admin','Admin'),
        ('agrivet','AgriVet'),
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=30, choices=ROLES)
    phone = models.CharField(_("phone number"), max_length=90)
    location = models.CharField(_("location"), max_length=100)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    is_active = models.BooleanField(_(""), default=False)
    is_staff = models.BooleanField(_(""), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email