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
        fields = ('email', 'first_name', 'last_name', 'user_type', 'property', 'phone_number', 'gender', 'marital_status', 'state_of_origin')
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
        marital_status=validated_data['marital_status']
        state_of_origin=validated_data['state_of_origin']
        gender=validated_data['gender']

        user = User.objects.create(email=email, user_type='manager')
        user.set_password(validated_data['password'])
        user.save()
        manager_obj = Manager.objects.create(user=user, first_name=first_name, last_name=last_name, phone_number=phone_number, gender=gender, marital_status=marital_status, state_of_origin=state_of_origin)
        validated_data['user_id']=user.id
        validated_data['email']=user.email
        validated_data['user_type']='manager'
        if property:
            
            for prop in property:
                manager_obj.property.add(prop)
                house = Property.objects.filter(id=prop.id).first()
                house.user = user
                house.all_managers.add(user)
                house.manager_vacant=False
                house.save(update_fields=['manager_vacant', 'user'])
        
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
        fields = ('email', 'first_name', 'last_name','user_type', 'phone_number', 'property', 'flat', 'payment', 'next_of_kin', 'former_address','next_of_kin_email', 'next_of_kin_number', 'next_of_kin_address')
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
        payment=attrs['payment']

        if not email:
            raise APIException400({"message": "email is required"})
        if User.objects.filter(email=email).exists():
            raise APIException400({"message": "This email already exists. Please login"})
        if Tenant.objects.filter(flat=flat, account_status=True).exists():
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
        next_of_kin=validated_data['next_of_kin']
        former_address=validated_data['former_address']
        next_of_kin_email=validated_data['next_of_kin_email']
        next_of_kin_number=validated_data['next_of_kin_number']
        next_of_kin_address=validated_data['next_of_kin_address']
        payments_data = validated_data.pop('payment')
        user = User.objects.create(email=email, user_type='tenant')
        user.set_password(validated_data['password'])
        user.save()
        tenant_obj = Tenant.objects.create(user=user, first_name=first_name, last_name=last_name, flat=flat, property=property, phone_number=phone_number, next_of_kin=next_of_kin, former_address=former_address, next_of_kin_email=next_of_kin_email, next_of_kin_number=next_of_kin_number,next_of_kin_address=next_of_kin_address)
        validated_data['user_id'] = user.id
        validated_data['email'] = user.email
        validated_data['user_type'] = 'tenant'

        for payment_data in payments_data:
            print(payment_data)
            payment = AddPayment.objects.create(**payment_data, property=property, tenant=user) 
            tenant_obj.payment.add(payment)
        prop=Property.objects.get(property_name=property)
        a=prop.id
       
        flat_update=Flat.objects.filter(test_id=a,name=flat).first()
        flat_update.vacant=False
        flat_update.current_tenant=user
        flat_update.all_tenants.add(user)
        flat_update.save(update_fields=['vacant', 'current_tenant'])

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
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo', instance.photo)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.permit_approval = validated_data.get('permit_approval', instance.permit_approval)
        instance.next_of_kin_name = validated_data.get('next_of_kin_name', instance.next_of_kin_name)
        instance.next_of_kin_email = validated_data.get('next_of_kin_email', instance.next_of_kin_email)
        instance.next_of_kin_number = validated_data.get('next_of_kin_number', instance.next_of_kin_number)
        instance.state_of_origin = validated_data.get('state_of_origin', instance.state_of_origin)
        instance.annual_salary = validated_data.get('annual_salary', instance.annual_salary)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.marital_status = validated_data.get('marital_status', instance.marital_status)
        instance.emergency_contact_info = validated_data.get('emergency_contact_info', instance.emergency_contact_info)

        instance.save()
        return instance
        
class LandlordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLord
        fields = ['first_name', 'last_name', 'phone_number','address', 'photo']

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo', instance.photo)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance
        
class DeactivateTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields=['user','account_status','flat','property']

    def update(self, instance, validated_data):
        instance.account_status = validated_data.get('account_status', instance.account_status)
        instance.flat=validated_data.get('flat', instance.flat)
        instance.property=validated_data.get('property', instance.property)
        instance.user=validated_data.get('user', instance.user)
        ten=Tenant.objects.get(flat=instance.flat)
        prop=Property.objects.filter(property_name=instance.property).first()
        a=prop.id
        b=instance.flat
        if instance.account_status==False:
            if Flat.objects.filter(current_tenant=instance.user).exists():
                flat_prop=Flat.objects.filter(current_tenant=instance.user).first()
                flat_prop.current_tenant=None
                flat_prop.vacant=True
                flat_prop.save(update_fields=['current_tenant', 'vacant'])
            else:
                raise APIException400({"message": "Tenant is not currently activated"})
        elif instance.account_status==True:
            vacancy = Flat.objects.filter(name=b, test_id=a, vacant=True).first()
            if vacancy:
                vacancy.current_tenant=instance.user
                vacancy.vacant=False
                vacancy.save(update_fields=['current_tenant', 'vacant'])
            else:
                raise APIException400({"message": "A Tenant is currently occupying this flat"})
            
        instance.save()

        return instance
        
class ActivateTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields=['user','account_status','flat','property']

    def update(self, instance, validated_data):
        instance.account_status = validated_data.get('account_status', instance.account_status)
        instance.flat=validated_data.get('flat', instance.flat)
        instance.property=validated_data.get('property', instance.property)
        instance.user=validated_data.get('user', instance.user)
        ten=Tenant.objects.get(flat=instance.flat)
        prop=Property.objects.filter(property_name=instance.property).first()
        a=prop.id
        b=instance.flat
        vacancy = Flat.objects.filter(name=b, test_id=a, vacant=True).first()
        if vacancy:
            vacancy.current_tenant=instance.user
            vacancy.vacant=False
            vacancy.save(update_fields=['current_tenant', 'vacant'])
        else:
            raise APIException400({"message": "A Tenant is currently occupying this flat"})
        instance.save()

        return instance
        
class DeactivateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields=['user','account_status']

    def update(self, instance, validated_data):
        instance.account_status = validated_data.get('account_status', instance.account_status)
        #instance.property=validated_data.get('property', instance.property)
        instance.user=validated_data.get('user', instance.user)
        #ten=Tenant.objects.get(flat=instance.flat)
        prop_id=self.context.get('request').parser_context.get('kwargs').get(
        'prop_id')
        prop=Property.objects.filter(id=prop_id).first()
        if instance.account_status==False:
            if Property.objects.filter(id=prop_id, user=instance.user).exists():
                prop_prop=Property.objects.filter(id=prop_id, user=instance.user).first()
                manager_prop=Manager.objects.filter(user=instance.user).first()
                manager_prop.property.remove(prop_prop)
                prop_prop.user=None
                prop_prop.manager_vacant=True
                prop_prop.save(update_fields=['user', 'manager_vacant'])
            else:
                raise APIException400({"message": "Manager is not currently activated"})
        elif instance.account_status==True:
            vacancy = Property.objects.filter(id=prop_id, manager_vacant=True).first()
            if vacancy:
                manager_prop=Manager.objects.filter(user=instance.user).first()
                manager_prop.property.add(vacancy)
                vacancy.user=instance.user
                vacancy.manager_vacant=False
                vacancy.save(update_fields=['user', 'manager_vacant'])
            else:
                raise APIException400({"message": "A Manager is currently in charge of this property"})
            
        instance.save()

        return instance
        
class ActivateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields=['user','account_status','property']

    def update(self, instance, validated_data):
        instance.account_status = validated_data.get('account_status', instance.account_status)
        instance.property=validated_data.get('property', instance.property)
        instance.user=validated_data.get('user', instance.user)
        #ten=Tenant.objects.get(flat=instance.flat)
        prop=Property.objects.filter(property_name=instance.property, user=instance).first()
        a=prop.id
        vacancy = Property.objects.filter(id=a, manager_vacant=True).first()
        if vacancy:
            vacancy.user=instance.user
            vacancy.manager_vacant=False
            vacancy.save(update_fields=['user', 'manager_vacant'])
        else:
            raise APIException400({"message": "A Manager is currently in charge this property"})
        instance.save()

        return instance
        
class ChangePasswordSerializer(serializers.Serializer):
    model = User
        

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
