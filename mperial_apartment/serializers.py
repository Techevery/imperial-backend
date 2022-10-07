from dataclasses import field
import email
from rest_framework import serializers
from mperial_apartment.models import *
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


#Property Serializer
# A serializer class that will be used to serialize the data.
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['property_name', 'address', 'property_image', 'flat_details', 'created', 'modified', 'approve']
        
    
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['name', 'phone_number', 'email', 'house_id', 'annual_salary']
        
        
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields=['tenant_name', 'tenant_phone_number', 'tenant_email', 'flat_id', 'property_id']
        

class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        model= Flat
        fields = ['flat_name', 'number_of_rooms', 'number_of_living_rooms', 'number_of_kitchens', 'number_of_toilets', 'description']

# Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id","username","email"]
    
    
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user