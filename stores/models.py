from django.db import models
from datetime import datetime

class Store(models.Model):
    name = models.TextField()
    address= models.TextField()
    phone = models.TextField()
    opening_hour = models.TextField()
    is_active =models.BooleanField()
    
    def __str__(self):
        return self.name
    

    