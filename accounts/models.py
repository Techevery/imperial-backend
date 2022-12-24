from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from api.models import Property, Flat, AddPayment
from tabnanny import verbose


# Create your models here.

class UserManager(BaseUserManager):
    """ User Manager that knows how to create users via email instead of username """
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

USER_TYPE = (('landlord', 'landlord'), ('tenant', 'tenant'), ('manager', 'manager'))
class User(AbstractUser):
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField(unique=True)
    is_landlord = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)

    def __str__(self):
        return str(self.email)

class LandLord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta():
        verbose_name_plural = 'LandLords'

    def __str__(self):
        return str(self.first_name)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    annual_salary = models.BigIntegerField()
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    property = models.ManyToManyField(Property, blank=True)
    permit_approval = models.BooleanField(null=True,blank=True,default=False)
    class Meta():
        verbose_name_plural = 'Manager'

    def __str__(self):
        return str(self.first_name)

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(blank=True, null=True, upload_to='uploads/tenant-pictures')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    flat = models.ForeignKey(Flat, related_name='Flat', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='House', on_delete=models.CASCADE)
    payment = models.ManyToManyField(AddPayment, related_name='AddPayment')
    annual_salary = models.BigIntegerField(null=True, blank=True)
    next_of_kin = models.CharField(max_length=100, null=True, blank=True)
    state_of_origin = models.CharField(max_length=100, null=True, blank=True)
    guarantor = models.CharField(max_length=100, null=True, blank=True)
    former_address = models.TextField(null=True, blank=True)
    place_of_work = models.CharField(max_length=100, null=True, blank=True)
    position_at_work = models.CharField(max_length=100, null=True, blank=True)
    purpose_of_rent = models.TextField(null=True, blank=True)


    class Meta():
        verbose_name_plural = 'Tenant'

    def __str__(self):
        return str(self.first_name)







