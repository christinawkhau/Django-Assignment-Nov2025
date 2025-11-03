
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address= models.CharField(max_length=100,blank=True, null=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    company = models.CharField(max_length=100,blank=True, null=True)
    role = models.CharField(max_length=100,blank=True, null=True)
    
        
    def __str__(self):
        return self.user.username 


