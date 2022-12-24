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
from .models import Flat, Property, MakePayment
from .models import Property
from django.shortcuts import get_object_or_404, redirect, render
from .serializer import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView
from accounts.models import Manager, Tenant
from accounts.serializer import *
from datetime import datetime, timedelta, time, date
from django.utils import timezone
import dateutil.parser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.user_type == 'landlord':
            token = super().get_token(user)

            # Add custom claims
            token['username'] = user.username
            # ...

            return token






class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class MyTokenObtainPairSerializer2(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.user_type == 'manager':
            token = super().get_token(user)

            # Add custom claims
            token['username'] = user.username
            # ...

            return token






class MyTokenObtainPairView2(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer2
    
class MyTokenObtainPairSerializer3(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.user_type == 'tenant':
            token = super().get_token(user)

            # Add custom claims
            token['username'] = user.username
            # ...

            return token






class MyTokenObtainPairView3(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer3

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
        flat = Flat.objects.get(id=id)
    except Flat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FlatSerializer(flat)
        return Response(serializer.data)
        
class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        serializer.data["data"] = "test"
        return Response(
             serializer.data
        )
class UserManager(APIView):
    def get(self, request):
        man=Manager.objects.get(user=request.user)
        serializer = ManagerSerializer(man)
        #serializer.data["data"] = "test"
        return Response(
             serializer.data
        )

@api_view(['GET'])
def managers_list(request):
    managers = Manager.objects.all()
    if request.method == 'GET':
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)
        
@api_view(['GET'])
def tenant_list(request):
    tenants = Tenant.objects.all()
    property = Property.objects.filter(flats__id=7)
    if request.method == 'GET':
        serializer_2 = PropertySerializer(property, many=True)
        serializer = TenantSerializer(tenants, many=True)
        for i in serializer.data:
            show = i['property']
            manager = Manager.objects.filter(property__id=show)
            seri = ManagerSerializer(manager, many=True)
            for man in seri.data:
                i.update({'manager':man})
        
            
        return Response({
            'data': serializer.data,
            
            
        })
        
@api_view(['GET'])
def tenants_list_manager(request):
    samp={}
    space=[]
    user_info = request.user
    tenants = Tenant.objects.all()
    if request.method == 'GET':
        if user_info.user_type == 'manager':
            man=Manager.objects.get(user=request.user)
            user_data=ManagerSerializer(man)
            a=user_data.data['user']
            for test in user_data.data['property']:
                tenants = Tenant.objects.filter(property=test)
                serializer = TenantSerializer(tenants, many=True)
                for i in serializer.data:
                    show = i['property']
                    property = Property.objects.filter(id=show)
                    serializer_2 = PropertySerializer(property, many=True)
                    for seri in serializer_2.data:
                        i.update({'property_details':seri})
                samp.update({"data":serializer.data})
                space.append(serializer.data)
        
                
                
            
            
        return Response(space)
        
@api_view(['GET'])
def tenants_list(request):
    tenants= Tenant.objects.all()
    if request.method == 'GET':
        serializer = TenantSerializer(tenants, many=True)
        for i in serializer.data:
            show = i['property']
            property = Property.objects.filter(id=show)
            serializer_2 = PropertySerializer(property, many=True)
            for seri in serializer_2.data:
                i.update({'property_details':seri})
    return Response(serializer.data)
        
        
        
class AddAccountCreateApi(CreateAPIView):
    serializer_class = AddAccountserializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save(user=request.user)

            return Response({
                'message': "Account added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)

class AssignAccountCreateApi(CreateAPIView):
    serializer_class = AssignAccountserializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Account assigned successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)

class AddExpensesCreateApi(CreateAPIView):
    serializer_class = AddExpensesserializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Expenses added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)
        
#Tenant
class AddDocumentCreateApi(CreateAPIView):
    serializer_class = AddDocumentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Document added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)

class AccountView(APIView):
    def get(self, request):
        account = AddAccount.objects.filter(user=request.user)
        if request.method == 'GET':
            serializer = AddAccountserializer(account, many=True)
            return Response(serializer.data)

class ExpensesView(APIView):
    def get(self, request):
        expenses = AddExpenses.objects.filter(user=request.user)
        if request.method == 'GET':
            serializer = AddExpensesserializer(expenses, many=True)
            total = 0
            for i in serializer.data:
                total = total + i['amount']

            return Response({'data':serializer.data,
                             'total': total
                             })

class ManagerProperty(APIView):
    def get(self, request, id):
        user_info = request.user
        if user_info.user_type == 'manager':
            property = Property.objects.get(pk=id)
            man=Manager.objects.get(user=request.user)
            user_data=ManagerSerializer(man)
        elif user_info.user_type == 'landlord':
            property = Property.objects.get(pk=id)
            serializer = PropertySerializer(property)
            

                
        
        if request.method == 'GET':
            serializer = PropertySerializer(property)
    
            for i in serializer.data['flats']:
                testing=i['id']
                tenant_data=Tenant.objects.filter(flat=testing).last()
                ten=TenantSerializer(tenant_data)
                tester=ten.data['user']
                i.update({
                    'full_name':ten.data['first_name']+' '+ten.data['last_name'],
                    'number':ten.data['phone_number'],
                    'tenant_id':ten.data['user']
                    #'dat':ten.data
                })
                count_down= AddPayment.objects.filter(tenant=tester, type="recurring").last()
                count= AddPayment.objects.filter(tenant=tester, type="recurring")
                pay = MakePayment.objects.filter(tenant=tester, status=True)
                pay_serializer = MakePaymentSerializer(pay, many=True)
                serializer_data = AddPaymentSerializer(count_down)
                expected_rent=AddPaymentSerializer(count,many=True)
                now=datetime.now()
                end = now+timedelta(days=2)
                tes = serializer_data.data["end_date"]
                datetime_date = dateutil.parser.parse(str(now))
                now= datetime_date.strftime("%Y-%m-%d")
                a="2022-12-30"
                if tes:
                    global real, test
                    real=datetime.strptime(tes,'%Y-%m-%d').date()
                    rea=datetime.strptime(now,'%Y-%m-%d').date()
                    test=str(real-rea)
                else:
                    test='0'
                paid=0
                years=0
                for pay in pay_serializer.data:
                    paid=paid+pay["amount"]
                expected_pay=0
                for pay in expected_rent.data:
                    expected_pay=expected_pay+pay["amount"]
                if expected_pay!=0:
                    if paid/expected_pay>=1:
                        years=years+(paid//expected_pay)
                test =str(test.split("days")[0])
                i.update({
                    #"now_4":test,
                    "amount_paid":paid,
                    #"ten":ten.data["payment"],
                    #"pay":pay_serializer.data,
                    "days_left":(int(test)+years)
                })
            a=serializer.data['user']
            man=Manager.objects.get(user=a)
            user_data=ManagerSerializer(man)
                
                
                
                        
                        
                
                
                
    
    
    
            return Response({
                'data':serializer.data,
                "property_name":serializer.data['property_name'],
                "image":serializer.data['property_image'],
                "address":serializer.data['address'],
                "manager":user_data.data['first_name'],
                "manager_number":user_data.data['phone_number'],
                #"expenses":total,
                #"debt":debt,
                #"total_sum":tenant_paid
            })
        else:
            return Response(status=404)
            
class LandlordProperty(APIView):
    def get(self, request, id):
        user_info = request.user
        if user_info.user_type == 'manager':
            property = Property.objects.get(pk=id)
            man=Manager.objects.get(user=request.user)
            user_data=ManagerSerializer(man)
        elif user_info.user_type == 'landlord':
            property = Property.objects.get(pk=id)
                
        
        if request.method == 'GET':
            serializer = PropertySerializer(property)
    
            for i in serializer.data['flats']:
                testing=i['id']
                tenant_data=Tenant.objects.filter(flat=testing).last()
                ten=TenantSerializer(tenant_data)
                tester=ten.data['user']
                i.update({
                    'full_name':ten.data['first_name']+' '+ten.data['last_name'],
                    'number':ten.data['phone_number'],
                    #'dat':ten.data
                })
                count_down= AddPayment.objects.filter(tenant=tester, type="recurring").last()
                count= AddPayment.objects.filter(tenant=tester, type="recurring")
                pay = MakePayment.objects.filter(tenant=tester, status=True)
                pay_serializer = MakePaymentSerializer(pay, many=True)
                serializer_data = AddPaymentSerializer(count_down)
                expected_rent=AddPaymentSerializer(count,many=True)
                now=datetime.now()
                end = now+timedelta(days=2)
                tes = serializer_data.data["end_date"]
                datetime_date = dateutil.parser.parse(str(now))
                now= datetime_date.strftime("%Y-%m-%d")
                a="2022-12-30"
                if tes:
                    global real, test
                    real=datetime.strptime(tes,'%Y-%m-%d').date()
                    rea=datetime.strptime(now,'%Y-%m-%d').date()
                    test=str(real-rea)
                else:
                    test='0'
                paid=0
                years=0
                for pay in pay_serializer.data:
                    paid=paid+pay["amount"]
                expected_pay=0
                for pay in expected_rent.data:
                    expected_pay=expected_pay+pay["amount"]
                if expected_pay!=0:
                    if paid/expected_pay>=1:
                        years=years+(paid/expected_pay)
                test =str(test.split("days")[0])
                i.update({
                    #"now_4":test,
                    "amount_paid":paid,
                    #"ten":ten.data["payment"],
                    #"pay":pay_serializer.data,
                    "days_left":(int(test)+years)
                })
            a=serializer.data['user']
            man=Manager.objects.get(user=a)
            user_data=ManagerSerializer(man)
                
                
                
                
                        
                        
                
                
                
    
    
    
            return Response({
                'data':serializer.data,
                "property_name":serializer.data['property_name'],
                "image":serializer.data['property_image'],
                "address":serializer.data['address'],
                "manager":user_data.data['first_name'],
                "manager_number":user_data.data['phone_number'],
                #"expenses":total,
                #"debt":debt,
                #"total_sum":tenant_paid
            })
        else:
            return Response(status=404)
                
class TenantDocument(APIView):
    def get(self, request):
        document = AddDocument.objects.filter(user=request.user.id)
        
        if request.method == 'GET':
            serializer = AddDocumentSerializer(document, many=True)
            
        return Response(serializer.data)
        
class TenantPaymentUpdate(APIView):
    def get(self, request):
        try:
            tenant = Tenant.objects.get(user=request.user)
        except Tenant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = TenantSerializer(tenant)
            seri = []
            for i in serializer.data['payment']:
                payment = AddPayment.objects.get(id=i)
                serial = AddPaymentSerializer(payment)
                seri.append(serial.data)

        return Response(seri)

class TenantDetails(APIView):
    permission_classes([IsAuthenticated])
    def get(self, request):
        print(request.user)

        tenant = Tenant.objects.get(user=request.user.id)
        prop = tenant.flat
        assigned_data = AssignAccount.objects.filter(flats=prop)
        item = []
        for ass in assigned_data:
            account_data = AddAccount.objects.get(id=ass.account.id)
            serializer_4 = AddAccountserializer(account_data)
            item.append(serializer_4.data)

        serializers_3 = AssignAccountSerializer(assigned_data, many=True)

        #account_data = AccountSerializer()

        serializer_2 = TenantSerializer(tenant)
        return Response(
            {'data': serializer_2.data,
             'assigned_account': item

             })
    
class MakePaymentView(CreateAPIView):
    serializer_class = MakePaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Payment added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)
        
class LandlordDocumentCreateApi(CreateAPIView):
    serializer_class = LandlordDocumentSerializer
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Document added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)
        
class ManagerFiles(APIView):
    def get(self, request):
        document = LandlordDocument.objects.filter(manager=request.user.id)
        if request.method == 'GET':
            serializer = LandlordDocumentSerializer(document, many=True)
            return Response(serializer.data)
        
class ManagerDocumentCreateApi(CreateAPIView):
    serializer_class = ManagerDocumentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Document added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)

class LandlordTenantDocCreateApi(CreateAPIView):
    serializer_class = LandlordTenantDocSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Document added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)
        
class TenantMyFilesCreateApi(CreateAPIView):
    serializer_class = AddDocumentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data,context={'request':request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            account = serializer.save()

            return Response({
                'message': "Document added successfully",
                'data': serializer.data,
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)
        
class ManagerDocumentView(APIView):
    def get(self, request):
        document = ManagerDocument.objects.filter(user=request.user.id)
        if request.method == 'GET':
            serializer = ManagerDocumentSerializer(document, many=True)
            return Response(serializer.data)
class TenantFiles(APIView):
    def get(self, request):
        try:
            document = LandlordTenantDoc.objects.filter(tenant=request.user.id)
        except LandlordTenantDoc.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        if request.method == 'GET':
            serializer = LandlordTenantDocSerializer(document, many=True)
            return Response(serializer.data)

class LandlordTenantFiles(APIView):
    def get(self, request, id):
        try:
            document = LandlordTenantDoc.objects.filter(tenant=id)
        except LandlordTenantDoc.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        if request.method == 'GET':
            serializer = LandlordTenantDocSerializer(document, many=True)
            return Response(serializer.data)
            
class LandlordTenantMyFiles(APIView):
    def get(self, request, id):
        document = AddDocument.objects.filter(user=id)
        
        if request.method == 'GET':
            serializer = AddDocumentSerializer(document, many=True)
            
        return Response(serializer.data)

class LandlordManagerMyFiles(APIView):
    def get(self, request, id):
        document = ManagerDocument.objects.filter(user=id)
        
        if request.method == 'GET':
            serializer = ManagerDocumentSerializer(document, many=True)
            
        return Response(serializer.data)
            
class ViewPayment(APIView):
    def get(self, request):
        #try:
        pay = MakePayment.objects.all()
        #except MakePayment.DoesNotExist:
        #return Response(status=status.HTTP_404_NOT_FOUND)

        
        if request.method == 'GET':
            serializer = MakePaymentSerializer(pay, many=True)
            return Response(serializer.data)
class ViewTenantPayment(APIView):
    def get(self, request, id):
        if request.method == 'GET':
            pay=MakePayment.objects.filter(tenant=id)
            serializer = MakePaymentSerializer(pay, many=True)
            return Response(serializer.data)
            
class PageView(APIView):
    #serializer_class = AddPaymentSerializer
    def get(self, request):
        tenant = Tenant.objects.get(user=request.user.id)
        ten=TenantSerializer(tenant)
        count_down = AddPayment.objects.filter(tenant=request.user.id, type="recurring").last()
        count= AddPayment.objects.filter(tenant=request.user.id, type="recurring")
        pay = MakePayment.objects.filter(tenant=request.user.id, status=True)
        pay_serializer = MakePaymentSerializer(pay, many=True)
        serializer_data = AddPaymentSerializer(count_down)
        expected_rent=AddPaymentSerializer(count,many=True)
        now=datetime.now()
        end = now+timedelta(days=2)
        #test=datetime.datetime.strptime(now,'%m/%d/%Y').date()
        final=str(end-now)
        tes = serializer_data.data["end_date"]
        datetime_date = dateutil.parser.parse(str(now))
        now= datetime_date.strftime("%Y-%m-%d")
        a="2022-12-30"
        if tes:
            global real, test
            real=datetime.strptime(tes,'%Y-%m-%d').date()
            rea=datetime.strptime(now,'%Y-%m-%d').date()
            test=str(real-rea)
        else:
            test=0
        paid=0
        years=0
        for pay in pay_serializer.data:
            paid=paid+pay["amount"]
        expected_pay=0
        for pay in expected_rent.data:
            expected_pay=expected_pay+pay["amount"]
        if paid/expected_pay>=1:
            years=years+(paid//expected_pay)
        test =str(test.split("days")[0])
            
            
        
        return Response({
             #"payment-data": serializer_data.data,
             #"days":final,
             #"now":now,
             #"now2": serializer_data.data["end_date"],
             #"now3":real,
             #"now_4":test,
             #"paid":paid,
             #"ten":ten.data["payment"],
             #"pay":pay_serializer.data,
             "days_left":(int(test)+years)
             
             
             })
             
class ManagerProp(APIView):
    def get(self, request):
        user_info = request.user
        if user_info.user_type == 'manager':
            #target=request.user.email
            property = Property.objects.filter(user=request.user)
            man=Manager.objects.get(user=request.user)
            user_data=ManagerSerializer(man)
            
        elif user_info.user_type == 'landlord':
            property = Property.objects.all()
        if request.method == 'GET':
            serializer = PropertySerializer(property, many=True)
            for i in serializer.data:
                data= i['id']
                head_id = i['user']
                expenses = AddExpenses.objects.filter(house=data)
                serializer_2 = AddExpensesserializer(expenses, many=True)
                payment = AddPayment.objects.filter(property=data,)
                paid = MakePayment.objects.filter(property=data)
                tenant = Tenant.objects.filter(property=data)
                serial_2 = AddPaymentSerializer(payment, many=True)
                serial_3 = MakePaymentSerializer(paid, many=True)
                tenant_paid=0
                for t in serial_3.data:
                    tenant_paid = tenant_paid + t['amount']
                    i.update({'paid':tenant_paid})
                sum =0
                for s in serial_2.data:
                    sum = sum + s['amount']
                    i.update({'Sum':sum})
                
                expense = 0
                for s in serializer_2.data:
                    expense = expense + s['amount']
                    i.update({'expenses':expense})
                debt= tenant_paid-sum
                i.update({
                    "debt":debt,
                    "total_sum":tenant_paid   
                })
                a=i['user']
                man=Manager.objects.filter(user=a).last()
                user_data=ManagerSerializer(man)
                i.update({
                    "manager":user_data.data['first_name']+' '+user_data.data['last_name']
                })
                
            
        return Response({
            #"property_name":serializer.data[0]['property_name'],
            #"image":serializer.data[0]['property_image'],
            #"address":serializer.data[0]['address'],
            #"manager":user_data.data['first_name'],
            #"expenses":expense,
            #"debt":debt,
            #"total_sum":tenant_paid,
            "data":serializer.data
            })
class TenantUpdate(APIView):
    def get(self, request):
        pass
    
class ApprovePayment(UpdateAPIView):
    serializer_class = ApprovePaymentSerializer
    permission_classes = [IsAuthenticated]
    model = MakePayment

    def put(self, request, id):
        instance = self.model.objects.get(pk=id)
        serialized_data = self.get_serializer(instance, data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)
        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)

    def patch(self, request, id):

        instance = self.model.objects.get(pk=id)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)
        