from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from . import forms
from .models import Flat, Property
from .models import Property
from django.shortcuts import get_object_or_404, redirect, render
from .serializer import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from accounts.models import Manager

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show(request):
    obj = [
        'a',
        'b',
    ]
    return Response(obj)

def add_property(request:HttpRequest) -> HttpResponse:
    if request.method == "POST":
        property_form = forms.AddPropertyForm(request.POST)
        if property_form.is_valid():
            prop = property_form.save(commit=False)

            prop.save()
            flat = Flat(
                name='testing',
                number_of_rooms=2,
                number_of_living_rooms=2,
                number_of_kitchens=2,
                number_of_toilets=2,
                description='testing',
                test_id=prop.id,

            )
            flat.save()
            f = Flat.objects.filter(test_id=prop.id)
            prop.flats.set(f)

            return redirect('show')

    else:
        property_form = forms.AddPropertyForm()
        context = {
            "property_form": property_form
        }
    return render(request, 'add_property.html', context)


class PropertyCreateApi(CreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            prop = serializer.save()
            print(prop)
            return Response({
                'message': "Property Created successfully",
                'data': serializer.data
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_property(request):
    if request.method == 'GET':
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)
        # return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def property_detail(request, id, format=None):
    try:
        property = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertySerializer(property)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def flat_detail(request, id, format=None):
    try:
        flat = Flat.objects.get(test_id=id)
    except Flat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FlatSerializer(flat)
        return Response(serializer.data)
        
class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@api_view(['GET'])
def managers_list(request):
    managers = Manager.objects.all()
    if request.method == 'GET':
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)
