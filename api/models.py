from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.
payment_type = (
    ('online payment', 'online_payment'),
    ('transfer', 'transfer')
)



class Flat(models.Model):
    name = models.CharField(max_length=100)
    number_of_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_living_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_kitchens = models.PositiveIntegerField(null=True, blank=True)
    number_of_toilets = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    test_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Property(models.Model):
    property_image = models.ImageField(blank=True, null=True, upload_to='uploads/properties')
    property_name = models.CharField(max_length=100)
    address = models.TextField()
    flats = models.ManyToManyField(Flat,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return str(self.property_name)
        
        
class AddPayment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.name)
        

class AddAccount(models.Model):
    account_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.PositiveIntegerField()
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.account_name)

class AssignAccount(models.Model):
    account = models.ForeignKey(AddAccount, related_name='Assignaccount', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    flats = models.ManyToManyField(Flat)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return str(self.account)


class AddExpenses(models.Model):
    amount = models.PositiveIntegerField()
    description = models.TextField()
    house = models.ForeignKey(Property, on_delete=models.CASCADE)
    receipt = models.FileField(upload_to='documents/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.house)
        

class AddDocument(models.Model):
    name = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/tenant-documents')
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
        
class MakePayment(models.Model):
    description = models.TextField()
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=100, choices=payment_type)
    ref_code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    receipt = models.FileField(upload_to='documents/tenant-payments', null=True, blank=True)
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.description
    
    

