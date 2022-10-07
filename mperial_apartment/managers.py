from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


# It creates a user with the given email and password.
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        """
        It creates a user with the given email and password, and returns the user
        
        :param email: The email address of the user
        :param password: The password to set for the user
        :return: The user object
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extral_fields):
        extral_fields.setdefault('is_staff', True)
        extral_fields.setdefault('is_superuser', True)
        extral_fields.setdefault('is_active',True)
        
        if extral_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extral_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extral_fields)
            
    
