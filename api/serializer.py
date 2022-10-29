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
from accounts.models import Manager, Tenant
# Register serializer
from rest_framework.exceptions import APIException
from drf_extra_fields.fields import Base64ImageField

User = get_user_model()

class APIException400(APIException):
    status_code = 400

class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flat
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    flats = FlatSerializer(many=True, error_messages={'required': "flat key is required", 'blank': "flat key can't be blank"})
    property_name = serializers.CharField(error_messages={'required': "property_name key is required", 'blank': "property_name key can't be blank"})
    address = models.TextField()
    property_image = Base64ImageField(required=False)
    class Meta:
        model = Property
        fields = '__all__'
        extra_kwargs = {'address': {'error_messages': {'blank': 'Address cannot be blank', 'required': "Address key is required"}}}

    def validate(self, attrs):
        flats = attrs['flats']
        property_name = attrs['property_name']
        address = attrs['address']



        if not flats:
            raise APIException400({"message": "property must have flats"})
        if not property_name:
            raise APIException400({"message": "property must have a name"})
        if not address:
            raise APIException400({"message": "property must have address"})

        return attrs

    def create(self, validated_data):
        property_name = validated_data['property_name']
        address = validated_data['address']
        property_image = validated_data['property_image']
        flats_data = validated_data.pop('flats')
        property = Property.objects.create(property_name=property_name, address=address, property_image=property_image)
        for flat_data in flats_data:
            print(flat_data)
            flat=Flat.objects.create(property=property, **flat_data, test_id=property.id)
            property.flats.add(flat)
            
        return property
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'
        
        
class AddPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddPayment
        fields = '__all__'
        
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'
        
        
class AddAccountserializer(serializers.ModelSerializer):
    account_name = serializers.CharField(error_messages={'required': "account_name key is required", 'blank': "account_name key can't be blank"})
    bank_name = serializers.CharField(error_messages={'required': "bank_name key is required", 'blank': "bank_name key can't be blank"})
    account_number = models.PositiveIntegerField(error_messages={'required': "account_number key is required", 'blank': "account_number key can't be blank"})
    class Meta:
        model = AddAccount
        fields = ['account_name', 'bank_name', 'account_number', 'comment', 'id']
        
        def validate(self, attrs):
            account_name = attrs['first_name']
            bank_name = attrs['last_name']
            account_number = attrs['property']


       
            if not account_name:
                raise APIException400({"message": "Account name is required"})
            if not bank_name:
                raise APIException400({"message": "Bank name is required"})
            if not account_number:
                raise APIException400({"message": "Account number is required"})
            
            return attrs

    def create(self, validated_data):
        account_name = validated_data['account_name']
        bank_name = validated_data['bank_name']
        account_number = validated_data['account_number']
        comment = validated_data['comment']
        user = self.context['request'].user
        addAccount = AddAccount.objects.create(account_name=account_name, account_number=account_number, bank_name=bank_name, comment=comment, user=user)
        return addAccount

class AssignAccountserializer(serializers.ModelSerializer):
    class Meta:
        model = AssignAccount
        fields = ['account', 'property', 'flats']

    def create(self, validated_data):
        account = validated_data['account']
        property = validated_data['property']
        flats_data = validated_data['flats']
        user = self.context['request'].user


        assignAccount = AssignAccount.objects.create(account=account, property=property, user=user)
        for flats in flats_data:
            assignAccount.flats.add(flats)

        return assignAccount

class AddExpensesserializer(serializers.ModelSerializer):
    class Meta:
        model = AddExpenses
        fields = ['amount', 'description', 'house', 'receipt']

    def create(self, validated_data):
        amount = validated_data['amount']
        description = validated_data['description']
        house = validated_data['house']
        receipt = validated_data['receipt']
        user = self.context['request'].user


        addExpenses = AddExpenses.objects.create(amount=amount, description=description, house=house, receipt=receipt, user=user)
        return addExpenses

class AssignAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignAccount
        fields = '__all__'

class AddDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddDocument
        fields = ['name', 'document', 'date']
        
    def create(self, validated_data):
        name = validated_data['name']
        document = validated_data['document']
        user = self.context['request'].user
        
        addDocument = AddDocument.objects.create(name=name, document=document, user=user)
        
        return addDocument
        
        
    

        
            
    
