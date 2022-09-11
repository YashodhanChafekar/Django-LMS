from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin 
)
from django.utils import timezone  
from django.utils.translation import gettext_lazy as _  
from .admin_manager import CustomAdminManager  

# Create your models here.
class Admin(AbstractBaseUser, PermissionsMixin):
    username = None  
    email = models.EmailField(_('email_address'), unique=True, max_length = 200)  
    date_joined = models.DateTimeField(auto_now_add=True)  
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True) 


    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []


    objects = CustomAdminManager()
      
    """ def has_perm(self, perm, obj=None):  
        return True  
  
    def is_staff(self):  
        return self.staff  
  
    @property  
    def is_admin(self):  
        return self.admin  
  
    def __str__(self):  
        return self.email """

    
class Book(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    isbn = models.CharField(max_length=50, null=False, blank=False)
    authors = models.CharField(max_length=300, null=True, blank=True)
    publisher = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        ordering = ['date']