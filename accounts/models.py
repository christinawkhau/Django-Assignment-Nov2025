
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.TextField()
    address= models.TextField()
    
    def __str__(self):
        return self.user.username 


