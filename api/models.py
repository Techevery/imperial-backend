from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.
payment_type = (
    ('online payment', 'online_payment'),
    ('transfer', 'transfer')
)
payment_option = (
    ('one-off', 'one-off'),
    ('recurring', 'recurring'),
    ('refundable', 'refundable')
)



class Flat(models.Model):
    name = models.CharField(max_length=100)
    number_of_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_living_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_kitchens = models.PositiveIntegerField(null=True, blank=True)
    number_of_toilets = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    test_id = models.IntegerField(null=True, blank=True)
    current_tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='active_tenant')
    all_tenants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='tenant_list')
    vacant = models.BooleanField(null=True, blank=True, default=True)

    def __str__(self):
        return str(self.name)


class Property(models.Model):
    property_image = models.ImageField(blank=True, null=True, upload_to='uploads/properties')
    property_name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    flats = models.ManyToManyField(Flat,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    


    def __str__(self):
        return str(self.property_name)
        
        
class AddPayment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=100, choices=payment_option, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return str(self.name)
        

class AddAccount(models.Model):
    account_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.PositiveIntegerField()
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

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
    flat_id = models.ForeignKey(Flat, on_delete=models.CASCADE, null=True, blank=True)
    receipt = models.FileField(upload_to='documents/')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="tenant_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(auto_now_add=False, auto_now=True)
    
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
    status = models.BooleanField(default=False, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE,null=True, blank=True)
    payment_date_and_time = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateField(auto_now_add=False, auto_now=True)
    approved_by = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.description
        
class PaySalary(models.Model):
    description = models.TextField()
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=100, choices=payment_type)
    ref_code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    receipt = models.FileField(upload_to='documents/salary-payments', null=True, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='user_manager')
    status = models.BooleanField(default=True, null=True, blank=True)
    manager_verify= models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    payment_date_and_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    
class LandlordDocument(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    document = models.FileField(upload_to='documents/landlord-documents')
    date = models.DateField(auto_now_add=True)
    house_id = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='manager_docs')
    
    def __str__(self):
        return str(self.name)
        
class ManagerDocument(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    document = models.FileField(upload_to='documents/manager-documents')
    date = models.DateField(auto_now_add=True)
    house_id = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
class LandlordTenantDoc(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    document = models.FileField(upload_to='documents/landlord-documents')
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='tenant_docs')
    
    def __str__(self):
        return str(self.name)

