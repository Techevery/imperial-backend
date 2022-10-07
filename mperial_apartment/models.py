
from enum import unique
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as BaseUsermanager

# Create your models here.

class Flat(models.Model):
    flat_name = models.CharField(max_length=200)
    number_of_rooms = models.PositiveIntegerField()
    number_of_living_rooms = models.PositiveIntegerField()
    number_of_kitchens = models.PositiveIntegerField()
    number_of_toilets = models.PositiveIntegerField()
    description = models.TextField(null=False)
    
    def __str__(self):
        return f'Flat: {self.flat_name}'
    
    class Meta():
        verbose_name_plural = 'Flat'
    

class Property(models.Model):
    property_name = models.CharField(max_length =200)
    address = models.CharField(max_length=200)
    property_image = models.ImageField(blank=True, null=True,  upload_to='uploads/properties')
    flat_details = models.ManyToManyField(Flat)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    approve = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Property: {self.property_name}'
    
    class Meta():
        verbose_name_plural = 'Property'
    
   
class Manager(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    house_id = models.ForeignKey(Property, on_delete=models.CASCADE) 
    annual_salary = models.BigIntegerField()
    
    def __Str__(self):
        return f'Manager: {self.first_name} {self.last_name}'
    
    class Meta():
        verbose_name_plural = 'Manager'
    

class Tenant(models.Model):
    tenant_name = models.CharField(max_length=200)
    tenant_phone_number = models.CharField(max_length=12)
    tenant_email = models.EmailField(max_length=100)
    flat_id = models.ForeignKey(Flat, related_name='Flat', on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, related_name='House', on_delete=models.CASCADE)
    
    class Meta():
        verbose_name_plural = 'Tenant'
    
