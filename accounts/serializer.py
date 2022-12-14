from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from phonenumber_field.formfields import PhoneNumberField
from django import forms
from django.db import transaction
from .models import *
from api.serializer import AddPaymentSerializer
import random
from string import digits, ascii_letters

# Register serializer
from rest_framework.exceptions import APIException
class APIException400(APIException):
    status_code = 400
    
def _pw(length=10):
    s = ''
    for i in range(length):
        s += random.choice(digits + ascii_letters)
    return s

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], password = validated_data['password'])
        return user

class RegisterLandlord(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], password = validated_data['password'])
        return user
# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','password')


raw_password = _pw()


class ManagerCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(error_messages={'required': "Email key is required", 'blank': "Email key can't be blank"})
    user_type = serializers.CharField(read_only=True)
    first_name = serializers.CharField(error_messages={'required': "first_name key is required", 'blank': "first_name key can't be blank"})
    last_name = serializers.CharField(error_messages={'required': "last_name key is required", 'blank': "last_name key can't be blank"})
    phone_number = PhoneNumberField()
    class Meta:
        model = Manager
        fields = ('email', 'first_name', 'last_name', 'user_type', 'property', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate(self, attrs):
        email = attrs['email']
        password = raw_password
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        property = attrs['property']

       
        if not email:
            raise APIException400({"message": "email is required"})
        if User.objects.filter(email=email).exists():
            raise APIException400({"message": "This email already exists. Please login"})
        for prop in property:
            if Manager.objects.filter(property=prop).exists():
                a =Property.objects.get(id=prop.id)
                raise APIException400({"message": "property " + a.property_name + " is already being managed"})
        if not first_name:
            raise APIException400({"message": "first_name is required"})
        if not last_name:
            raise APIException400({"message": "last_name is required"})
        if not password:
            raise APIException400({"message": "password is required"})
        if len(password) < 8:
            raise APIException400({'message': "Password must be of atleast 8 characters"})
        property = []
        return attrs

    def create(self, validated_data):

        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        validated_data['password'] = raw_password
        phone_number = validated_data['phone_number']
        property = validated_data['property']

        user = User.objects.create(email=email, user_type='manager')
        user.set_password(validated_data['password'])
        user.save()
        manager_obj = Manager.objects.create(user=user, first_name=first_name, last_name=last_name, annual_salary=1000, phone_number=phone_number)
        validated_data['user_id']=user.id
        validated_data['email']=user.email
        validated_data['user_type']='manager'
        if property:
            
            for prop in property:
                manager_obj.property.add(prop)
                house = Property.objects.get(id=prop.id)
                house.user = user
                house.save()
        
        return validated_data



class LandlordCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={'required': "Email key is required", 'blank': "Email key can't be blank"})
    password = serializers.CharField(error_messages={'required': "password key is required", 'blank': "password key can't be blank"})
    user_type = serializers.CharField(read_only=True)
    
    class Meta:
        model = LandLord
        fields = '__all__'


    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
       
        if not email:
            raise APIException400({"message": "email is required"})
        if User.objects.filter(email=email).exists():
            raise APIException400({"message": "This email already exists. Please login"})
        if not password:
            raise APIException400({"message": "password is required"})
        if len(password) < 8:
            raise APIException400({'message': "Password must be of atleast 8 characters"})
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create(email=email, user_type='landlord')
        user.set_password(validated_data['password'])
        user.save()
        landlord_obj = LandLord.objects.create(user=user, first_name="test")
        validated_data['user_id']=user.id
        validated_data['email']=user.email
        validated_data['user_type']='landlord'
        return validated_data
        
        
class TenantCreateSerializer(serializers.ModelSerializer):
    payment = AddPaymentSerializer(many=True, required=False)
    email = serializers.EmailField(
        error_messages={'required': "Email key is required", 'blank': "Email key can't be blank"})
    first_name = serializers.CharField(
        error_messages={'required': "first_name key is required", 'blank': "first_name key can't be blank"})
    last_name = serializers.CharField(
        error_messages={'required': "last_name key is required", 'blank': "last_name key can't be blank"})
    phone_number = PhoneNumberField()
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = Tenant
        fields = ('email', 'first_name', 'last_name','user_type', 'phone_number', 'property', 'flat', 'payment')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate(self, attrs):
        email = attrs['email']
        password = raw_password
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        property = attrs['property']
        flat = attrs['flat']

        if not email:
            raise APIException400({"message": "email is required"})
        if User.objects.filter(email=email).exists():
            raise APIException400({"message": "This email already exists. Please login"})
        if Tenant.objects.filter(flat=flat).exists():
            raise  APIException400({"message": "Tenant currently occupying this flat"})
        if not first_name:
            raise APIException400({"message": "first_name is required"})
        if not last_name:
            raise APIException400({"message": "last_name is required"})
        if not password:
            raise APIException400({"message": "password is required"})
        if len(password) < 8:
            raise APIException400({'message': "Password must be of atleast 8 characters"})
        return attrs

    def create(self, validated_data):

        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        validated_data['password'] = raw_password
        property = validated_data['property']
        flat = validated_data['flat']
        phone_number = validated_data['phone_number']
        payments_data = validated_data.pop('payment')
        user = User.objects.create(email=email, user_type='tenant')
        user.set_password(validated_data['password'])
        user.save()
        tenant_obj = Tenant.objects.create(user=user, first_name=first_name, last_name=last_name, flat=flat, property=property, phone_number=phone_number)
        validated_data['user_id'] = user.id
        validated_data['email'] = user.email
        validated_data['user_type'] = 'tenant'

        for payment_data in payments_data:
            print(payment_data)
            payment = AddPayment.objects.create(**payment_data)
            tenant_obj.payment.add(payment)
        flat_update = Flat.objects.get(id=flat)
        flat_update.vacant = True
        flat_update.update()

        return validated_data
        
        
class TenantChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['photo', 'first_name', 'last_name', 'phone_number', 'next_of_kin', 'state_of_origin', 'guarantor', 'position_at_work', 'annual_salary', 'former_address', 'purpose_of_rent']

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo', instance.photo)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.next_of_kin = validated_data.get('next_of_kin', instance.next_of_kin)
        instance.state_of_origin = validated_data.get('state_of_origin', instance.state_of_origin)
        instance.guarantor = validated_data.get('guarantor', instance.guarantor)
        instance.position_at_work = validated_data.get('position_at_work', instance.position_at_work)
        instance.annual_salary = validated_data.get('annual_salary', instance.annual_salary)
        instance.former_address = validated_data.get('former_address', instance.former_address)
        instance.purpose_of_rent = validated_data.get('purpose_of_rent', instance.purpose_of_rent)

        instance.save()
        return instance
        
class ManagerChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['first_name', 'last_name', 'phone_number']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        return instance
