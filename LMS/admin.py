from django.contrib import admin
from .models import Admin, Book

from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import admin  
from django.contrib.auth import authenticate  
from django.contrib.auth.admin import UserAdmin 



# Register your models here.


 
# Register your models here.  
class CustomUserAdmin(UserAdmin):  
    add_form = CustomUserCreationForm  
    form = CustomUserChangeForm  
    model = Admin  
  
    list_display = ('email', 'is_staff', 'is_active',)  
    list_filter = ('email', 'is_staff', 'is_active',)  
    fieldsets = (  
        (None, {'fields': ('email', 'password')}),  
        ('Permissions', {'fields': ('is_staff', 'is_active')}),  
    )  
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}  
        ),  
    )  
    search_fields = ('email',)  
    ordering = ('email',)  
    filter_horizontal = ()  
  
admin.site.register(Admin, CustomUserAdmin) 

admin.site.register(Book)
