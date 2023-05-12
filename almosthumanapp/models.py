from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin 
from django.utils import timezone  
from django.utils.translation import gettext_lazy as _  
from .manager import CustomUserManager
# Create your models here.




class User(AbstractBaseUser,PermissionsMixin):
    username  = models.CharField(max_length=255,default="")
    email 		= models.EmailField(_('email'),unique=True)
    password    = models.CharField(max_length=255,default="")
    is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
    role = models.CharField(max_length=255,default="")
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)


    

    USERNAME_FIELD 	='email'
    objects 		= CustomUserManager()
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
      
      
      
class Stripe_subscription(models.Model):
  
  user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  subscription_id = models.CharField(max_length=500,default="")
  price_id = models.CharField(max_length=500,default="")
  created_at = models.DateTimeField(auto_now_add=True,null=True)
  updated_at =  models.DateTimeField(auto_now=True)      
  