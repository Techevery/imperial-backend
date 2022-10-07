from django.http import JsonResponse
from django.http import HttpResponse
from mperial_apartment.models import *
from mperial_apartment.serializers import *
from rest_framework import  status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer


# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello! </h1>")

@api_view(['GET', 'POST'])
def get_property(request, format=None):
    
    if request.method == 'GET':
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return JsonResponse({"properties": serializer.data})
        # return Response(serializer.data)
    
    elif request.method == 'POST':
       serializer= PropertySerializer(data=request.data)
       
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def property_detail(request, id, format=None):
    
    try:
       property =  Property.objects.get(pk=id)
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
    
    
    
@api_view(['GET','POST'])
def get_flat(request,format=None):
    
    if request.method == 'GET':
        flat = Flat.objects.all()
        serializer = FlatSerializer(flat, many=True)
        return JsonResponse({"flat":serializer.data})
    
    elif request.method == 'POST':
        serializer = FlatSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
        
        
        
@api_view(['GET','PUT','DELETE'])
def flat_detail(request, id, format=None):
    
    try:
        flat = Flat.objects.get(pk=id)
    except Flat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FlatSerializer(flat)
        return Response(serializer.data)
    
    elif request.method =='PUT':
        serializer = FlatSerializer(flat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        flat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET','POST'])
def get_manager(request,format=None):
    if request.method == 'GET':
        manager = Manager.objects.all()
        serializer = ManagerSerializer(manager, many=True)
        return JsonResponse({"manager":serializer.data})
    
    elif request.method == 'POST':
        serializer = ManagerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def manager_detail(request, id, format=None):
    
    try:
       property =  Manager.objects.get(pk=id)
    except Manager.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    
    if request.method == 'GET':
        serializer = ManagerSerializer(property)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ManagerSerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','POST'])
def get_tenant(request,format=None):
    if request.method == 'GET':
        manager = Tenant.objects.all()
        serializer = TenantSerializer(manager, many=True)
        return JsonResponse({"tenant":serializer.data})
    
    elif request.method == 'POST':
        serializer = TenantSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def tenant_detail(request, id, format=None):
    
    try:
       property =  Tenant.objects.get(pk=id)
    except Tenant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    
    if request.method == 'GET':
        serializer = TenantSerializer(property)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TenantSerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



    

    
    

@api_view(['GET','POST'])
def manager_view(request):
    
    if request.method == 'GET':
        manager = Manager.objects.all()
        serializer = ManagerSerializer(manager, many=True)
        
        
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

        
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    