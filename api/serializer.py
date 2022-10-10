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
# Register serializer
from rest_framework.exceptions import APIException

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
    class Meta:
        model = Property
        fields = '__all__'
        extra_kwargs = {'address': {'error_messages': {'blank': 'Address cannot be blank', 'required': "Address key is required"}}}

    def validate(self, attrs):
        flats = attrs['flats']
        property_name = attrs['property_name']
        property_image = attrs['property_image']
        address = attrs['address']



        if not flats:
            raise APIException400({"message": "property must have flats"})
        if not property_name:
            raise APIException400({"message": "property must have a name"})
        if not property_image:
            raise APIException400({"message": "property must have image"})
        if not address:
            raise APIException400({"message": "property must have address"})

        return attrs

    def create(self, validated_data):
        flats_data = validated_data.pop('flats')
        property = Property.objects.create(**validated_data)
        for flat_data in flats_data:
            test = property.id
            print(test)
            Flat.objects.create(property=property,  **flat_data, test_id=test)

            return property
