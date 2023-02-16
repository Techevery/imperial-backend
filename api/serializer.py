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
from accounts.models import Manager, Tenant, LandLord
# Register serializer
from rest_framework.exceptions import APIException
from drf_extra_fields.fields import Base64ImageField, Base64FileField
import base64
from io import BytesIO
from PIL import Image
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

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
        b=[]
        for flat in flats:
            a=flat['name']
            #if Flat.objects.filter(name=a).exists():
                #raise APIException400({"message": "flat name exists"})
            if a not in b:
                b.append(a)
            else:
                raise APIException400({"message": "property can not have flats with similar name"})
            

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
            
    
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLord
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
        fields = ['amount', 'description', 'house','receipt']

    def create(self, validated_data):
        amount = validated_data['amount']
        description = validated_data['description']
        house = validated_data['house']
        receipt = validated_data['receipt']
        user = self.context['request'].user


        addExpenses = AddExpenses.objects.create(amount=amount, description=description, house=house,receipt=receipt, user=user)
        return addExpenses

class AssignAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignAccount
        fields = '__all__'

#Tenant
class AddDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddDocument
        fields = ['id','name', 'document', 'date']
        
    def create(self, validated_data):
        name = validated_data['name']
        document = validated_data['document']
        user = self.context['request'].user
        
        addDocument = AddDocument.objects.create(name=name, document=document, user=user)
        
        return addDocument
        
def validate_document_file(value):
    try:
        # Check if the file is base64 encoded
        if "data:" not in value:
            raise serializers.ValidationError("Not a valid document")
        format, docstr = value.split(";base64,")
        ext = format.split("/")[-1]
        # Decode the base64 encoded file
        decoded_file = base64.b64decode(docstr)
        # Check if the decoded file is a valid document format
        if ext not in ["pdf", "doc", "docx", "txt"]:
            raise serializers.ValidationError("Not a valid document")
        # Return the decoded file
        return decoded_file
    except:
        raise serializers.ValidationError("Not a valid document")
        
class Base64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            logger.warning(e)
        else:
            return 'pdf'

class MakePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakePayment
        fields = '__all__'
        
        
    def validate(self, attrs):
        description = attrs['description']
        amount = attrs['amount']
        type = attrs['type']
        
        
        if not description:
            raise APIException400({"message": "please enter a description"})
        if not amount:
            raise APIException400({"message": "please enter a valid amount"})
        if not type:
            raise APIException400({"message": "please specify a type"})
        
            
                
        return attrs
                
    def create(self, validated_data):
        
        description = validated_data['description']
        amount = validated_data['amount']
        type = validated_data['type']
        receipt = validated_data['receipt']
        ref_code = validated_data['ref_code']
        tenant = self.context['request'].user
        obj = Tenant.objects.get(user=tenant)
        obj_1= Property.objects.get(flats=obj.flat)
        
        pay = MakePayment.objects.create(description=description, amount=amount, type=type, ref_code=ref_code, receipt=receipt, tenant=tenant, property=obj_1)
        
        return pay
        
class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaySalary
        fields = '__all__'
        
        
    def validate(self, attrs):
        description = attrs['description']
        amount = attrs['amount']
        type = attrs['type']
        ref_code = attrs['ref_code']
        receipt = attrs['receipt']
        
        if not amount:
            raise APIException400({"message": "please enter a valid amount"})
        if type == 'transfer':
            if not receipt:
                raise APIException400({"message": "please provide receipt for payment by transfer"})
                
        if type == 'online payment':
            if not ref_code:
                raise APIException400({"message": "please generate a ref code"})
                
        return attrs
                
    def create(self, validated_data):
        description = validated_data['description']
        amount = validated_data['amount']
        type = validated_data['type']
        ref_code = validated_data['ref_code']
        receipt = validated_data['receipt']
        manager = validated_data['manager']
        user = self.context['request'].user
        if type=='transfer':
            status=True
        else:
            status=False
        #obj = Tenant.objects.get(user=tenant)
        #obj_1= Property.objects.get(flats=obj.flat)
        
        pay = PaySalary.objects.create(description=description, amount=amount, type=type, ref_code=ref_code, receipt=receipt, status=status, manager=manager,user=user)
        return pay
        
class LandlordDocumentSerializer(serializers.ModelSerializer):
    #test = User.objects.get(id=66)
    class Meta:
        model = LandlordDocument
        fields = ['id','name', 'document', 'date', 'manager']
        
    def create(self, validated_data):
        name = validated_data['name']
        document = validated_data['document']
        #house_id = validated_data['house_id']
        manager = validated_data['manager']
        user = self.context['request'].user
        
        addDocument = LandlordDocument.objects.create(name=name, document=document, manager=manager, user=user)
        
        return addDocument
    
class ManagerDocumentSerializer(serializers.ModelSerializer):
    #test = User.objects.get(id=66)
    class Meta:
        model = ManagerDocument
        fields = ['id','name', 'document', 'date']
        
    def create(self, validated_data):
        name = validated_data['name']
        document = validated_data['document']
        user = self.context['request'].user
        
        addDocument = ManagerDocument.objects.create(name=name, document=document, user=user)
        
        return addDocument
        
class LandlordTenantDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordTenantDoc
        fields = ['id','name', 'document', 'date','tenant']
        
    def create(self, validated_data):
        name = validated_data['name']
        document = validated_data['document']
        tenant = validated_data['tenant']
        user = self.context['request'].user
        
        addDocument = LandlordTenantDoc.objects.create(name=name, document=document, tenant=tenant, user=user)
        
        return addDocument
class ApprovePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakePayment
        fields = ['status']
        
    def validate(self, attrs):
        user_data = self.context['request'].user
        if user_data.user_type=="manager":
            man=Manager.objects.get(user=user_data)
            if man.permit_approval !=True:
                raise APIException400({"message": "Manager does not have access to approve payment"})
        return attrs

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
        
class ApproveSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaySalary
        fields = ['manager_verify']

    def update(self, instance, validated_data):
        instance.manager_verify = validated_data.get('manager_verify', instance.manager_verify)
        instance.save()
        return instance
        
class EditPropertySerializer(serializers.ModelSerializer):
    property_image = Base64ImageField(required=False)
    class Meta:
        model = Property
        fields = ['property_name', 'user' ,'address','property_image']
        
        
    def update(self, instance, validated_data):
        instance.property_name = validated_data.get('property_name', instance.property_name)
        instance.property_image = validated_data.get('property_image', instance.property_image)
        instance.address = validated_data.get('address', instance.address)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
        
class DeleteFlatFromProp(serializers.ModelSerializer):
    flats = FlatSerializer(many=True)
    class Meta:
        model = Property
        fields = '__all__'
        
    def get_or_create_flatss(self, flatss):
        flats_ids = []
        for flats in flatss:
            flats_instance, created = Flats.objects.get_or_create(pk=flats.get('id'), defaults=flats)
            flats_ids.append(flats_instance.pk)
        return flats_ids

    def create_or_update_flatss(self, flatss):
        flats_ids = []
        for flats in flatss:
            flats_instance, created = Flats.objects.update_or_create(pk=flats.get('id'), defaults=flats)
            flats_ids.append(flats_instance.pk)
        return flats_ids

    def create(self, validated_data):
        flats = validated_data.pop('flats', [])
        property = Property.objects.create(**validated_data)
        property.flats.set(self.get_or_create_flatss(flats))
        return order

    def update(self, instance, validated_data):
        flats = validated_data.pop('flats', [])
        instance.flats.set(self.create_or_update_flatss(flats))
        fields = ['test_id']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
        return instance
        
class EditFlatFromProp(serializers.Serializer):
    flats = FlatSerializer(many=True)
    class Meta:
        fields=("flats",)
        
    def create(self, validated_data):
        flats_data = validated_data.pop('flats')
        #prop_id = self.context['view'].kwargs.get('id')
        prop_id=self.context.get('request').parser_context.get('kwargs').get(
        'id') 
        property=Property.objects.filter(id=prop_id).last()
        for flat_data in flats_data:
            print(flat_data)
            flat=Flat.objects.create(**flat_data, test_id=prop_id)
            property.flats.add(flat)
            
        return property

        
        
   
        

            
    
