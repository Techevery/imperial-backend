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
from .models import Flat, Property, MakePayment, PaySalary
from .models import Property
from django.shortcuts import get_object_or_404, redirect, render
from .serializer import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView
from accounts.models import Manager, Tenant, LandLord
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

def home(request):
    return render(request, "home.html")

def manager_web(request):
    return render(request, "tables.html")

def property_web(request):
    return render(request, "properties.html")

def manager_detail_web(request):
    return render(request, "billing.html")

def property_detail_web(request):
    return render(request, "property_detail.html")




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


#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
class AllProperties(APIView):
    def get(self, request):
        if request.method == 'GET':
            properties = Property.objects.all()
            serializer = PropertySerializer(properties, many=True)
            for i in serializer.data:
                man=i['user']
                manager=Manager.objects.filter(user=man).last()
                serial=ManagerSerializer(manager)
                num_flats=0
                occupied_in_flats=0
                prop_id=i['id']
                flat = Flat.objects.filter(test_id=prop_id)
                for num_flat in flat:
                    num_flats=num_flats+1
                    if num_flat.vacant==False:
                        occupied_in_flats=occupied_in_flats+1
                i.update({
                    "flats":num_flats,
                    "occupied":occupied_in_flats,
                    "manager_name":serial.data['first_name']+' '+serial.data['last_name'],
                    "manager_number":serial.data['phone_number']
                })
                
                
            return Response(serializer.data)
            # return Response(serializer.data)
            
class PropertyNoManager(APIView):
    def get(self, request):
        if request.method == 'GET':
            properties = Property.objects.filter(user__isnull=True)
            serializer = PropertySerializer(properties, many=True)
            
            return Response(serializer.data)


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
class UserLandlord(APIView):
    def get(self, request):
        landlord=LandLord.objects.get(user=request.user)
        user_serializer=LandlordSerializer(landlord)
        
        serializer=UserSerializer(request.user)
        first_name=user_serializer['first_name']
        return Response({
            "email":serializer.data['email'],
            "more_info":user_serializer.data
        })
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
        
#@api_view(['GET'])
class TenantList(APIView):
    def get(self, request):
        user_info = request.user
        if user_info.user_type == 'manager':
            target=request.user
            man=Manager.objects.filter(user=target).first()
            man_serial = ManagerSerializer(man)
            #for man_prop in man_serial.data['property']:
            tenants=Tenant.objects.filter(property__in=man_serial.data['property'])
            #tenants.append(a)
            #man=Manager.objects.get(user=request.user)
            #user_data=ManagerSerializer(man)
            
        elif user_info.user_type == 'landlord':
            tenants= Tenant.objects.all()
        if request.method == 'GET':
            serializer = TenantSerializer(tenants, many=True)
            for i in serializer.data:
                show = i['property']
                tester=i['user']
                property = Property.objects.filter(id=show)
                serializer_2 = PropertySerializer(property, many=True)
                count_down= AddPayment.objects.filter(tenant=tester, type="recurring").last()
                count= AddPayment.objects.filter(tenant=tester, type="recurring")
                count_1= AddPayment.objects.filter(tenant=tester, type="recurring")
                count_2= AddPayment.objects.filter(tenant=tester, type="refundable")
                pay = MakePayment.objects.filter(tenant=tester, status=True)
                pay_serializer = MakePaymentSerializer(pay, many=True)
                serializer_data = AddPaymentSerializer(count_down)
                expected_rent=AddPaymentSerializer(count,many=True)
                optional_pay=AddPaymentSerializer(count_2,many=True)
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
                optional_total=0
                for pay in expected_rent.data:
                    expected_pay=expected_pay+pay["amount"]
                for amount in optional_pay.data:
                    optional_total=optional_total+amount['amount']
                if expected_pay!=0:
                    if paid/expected_pay>=1:
                        years=years+(paid//expected_pay)
                if 's' in test:
                    test =str(test.split("days")[0])
                else:
                    test =str(test.split("day")[0])
                    
                if test=="0:00:00":
                    test="0"
                #test =str(test.split("days")[0])
                if paid>=expected_pay:
                    i.update({
                        "rent_status":"paid",
                        "debt":0
                    })
                else:
                    debt=expected_pay-paid
                    i.update({
                        "rent_status":"owing",
                        "debt":debt
                    })
                i.update({
                    #"now_4":test,
                    "amount_paid":paid,
                    #"ten":ten.data["payment"],
                    #"pay":pay_serializer.data,
                    "days_left":(int(test)+years),
                    "re-occuring":expected_pay,
                    "refundable":optional_total,
                    "start_date":serializer_data.data['start_date'],
                    "end_date":serializer_data.data['end_date']
                })
                for seri in serializer_2.data:
                    manager_id=seri['user']
                    if manager_id:
                        
                        man=Manager.objects.get(user=manager_id)
                        serial_manager = ManagerSerializer(man)
                    
                        i.update({
                            'property_details':seri,
                            'manager_details':serial_manager.data
                                })
                    else:
                        i.update({
                            'property_details':seri,
                            'manager_details':{"user": "null",
            "first_name": "null",
            "last_name": "null",
            "photo": "null",
            "address": "null",
            "annual_salary": "null",
            "phone_number": "null",
            "permit_approval": "false",
            "account_status": "false",
            "property": [
               
            ]
        }
                                })
                        
                
                        
        return Response(serializer.data)
        
class TenantViewLandlord(APIView):
    def get(self, request):
        obj = request.user
        tenant=Tenant.objects.filter(user=obj).first()
        if request.method == 'GET':
            serializer = TenantSerializer(tenant)
            man=serializer.data['property']
            manager=Manager.objects.filter(property=man).first()
            man_serial= ManagerSerializer(manager)
            
            return Response({
                "data":man_serial.data
            })
        
        
        
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
        user_info = request.user
        if user_info.user_type == 'manager':
            expenses = AddExpenses.objects.filter(user=request.user)
        else:
            expenses = AddExpenses.objects.all()
        if request.method == 'GET':
            serializer = ExpensesSerializer(expenses, many=True)
            total = 0
            for i in serializer.data:
                total = total + i['amount']

            return Response({'data':serializer.data,
                             'total': total
                             })
                             
class ApproveExpenseAPIView(generics.UpdateAPIView):
    queryset = AddExpenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        expense_id = self.kwargs['pk']
        expense = get_object_or_404(AddExpenses, pk=expense_id)
        if expense.approved_status:
            return Response({'message': 'Expense has already been approved.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            current_datetime = datetime.now()
            current_date = current_datetime.date()  # Extract the date portion from the current date/time
            serializer.save(approved_date=current_date, approved_status=True)
            return Response({'message': 'Expense has been approved.'}, status=status.HTTP_200_OK)

class ExpensesFlatView(APIView):
    def get(self, request, id):
        user_info = request.user
        if user_info.user_type == 'manager':
            expenses = AddExpenses.objects.filter(tenant=id, user=request.user)
        else:
            expenses = AddExpenses.objects.filter(tenant=id)
        if request.method == 'GET':
            serializer = AddExpensesserializer(expenses, many=True)
            total = 0
            for i in serializer.data:
                total = total + i['amount']

            return Response({'data':serializer.data,
                             'total': total
                             })
                             
class ManagerExpensesView(APIView):
    def get(self, request, id):
        user_info = request.user
        if user_info.user_type == 'manager':
            expenses = AddExpenses.objects.filter(house=id)
        else:
            expenses = AddExpenses.objects.filter(house=id)
        if request.method == 'GET':
            serializer = ExpensesSerializer(expenses, many=True)
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
                count_1= AddPayment.objects.filter(tenant=tester, type="recurring")
                count_2= AddPayment.objects.filter(tenant=tester, type="refundable")
                count_3=AddPayment.objects.filter(tenant=tester, type="one-off")
                pay = MakePayment.objects.filter(tenant=tester, status=True)
                pay_serializer = MakePaymentSerializer(pay, many=True)
                serializer_data = AddPaymentSerializer(count_down)
                expected_rent=AddPaymentSerializer(count,many=True)
                optional_pay=AddPaymentSerializer(count_2,many=True)
                one_off =AddPaymentSerializer(count_3, many=True)
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
                optional_total=0
                one_off_total=0
                for pay in expected_rent.data:
                    expected_pay=expected_pay+pay["amount"]
                for amount in optional_pay.data:
                    optional_total=optional_total+amount['amount']
                for amount in one_off.data:
                    one_off_total=one_off_total+amount['amount']
                if expected_pay!=0:
                    if paid/(expected_pay+one_off_total)>=1:
                        years=years+((((paid-one_off_total)//expected_pay)-1)*365)
                if 's' in test:
                    test =str(test.split("days")[0])
                else:
                    test =str(test.split("day")[0])
                    
                if test=="0:00:00":
                    test="0"
                if paid>=expected_pay:
                    i.update({
                        "rent_status":"paid",
                        "debt":0
                    })
                else:
                    #test='0'
                    debt=expected_pay-paid
                    i.update({
                        "rent_status":"owing",
                        "debt":debt
                    })
                check=(int(test)+years)
                if check<0:
                    value=(check//365)
                    debt = value*expected_pay
                    debt=(debt+paid-expected_pay)
                    i.update({
                        "debt":debt,
                        "rent_status":"owing"
                    })
                    
                i.update({
                    #"now_4":test,
                    "amount_paid":paid,
                    #"ten":ten.data["payment"],
                    #"pay":pay_serializer.data,
                    "days_left":(int(test)+years),
                    "re-occuring":expected_pay,
                    "refundable":optional_total
                })
                if tenant_data==None:
                    i.update({
                        "days_left":0
                    })
            a=serializer.data['user']
            man=Manager.objects.filter(user=a).first()
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
                        years=years+(((paid//expected_pay)-1)*365)
                test =str(test.split("days")[0])
                if test=="0:00:00":
                    test="0"
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

class TenantDocdelete(APIView):
   def delete(self, request, id):
        doc = AddDocument.objects.filter(pk=id)
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class LandlordDelManagerdoc(APIView):
    def delete(self, request, id):
        doc = LandlordDocument.objects.filter(pk=id)
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class TenantPaymentUpdate(APIView):
    def get(self, request):
        try:
            tenant = Tenant.objects.get(user=request.user)
        except Tenant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = TenantSerializer(tenant)
            #user_id=serializer["user"]
            payment_1=AddPayment.objects.filter(tenant=request.user)
            one_off=AddPayment.objects.filter(tenant=request.user, type="one-off")
            recurring=AddPayment.objects.filter(tenant=request.user, type="recurring")
            refundable=AddPayment.objects.filter(tenant=request.user, type="refundable")
            serial=AddPaymentSerializer(payment_1, many=True)
            serial_1=AddPaymentSerializer(one_off, many=True)
            serial_2=AddPaymentSerializer(recurring, many=True)
            serial_3=AddPaymentSerializer(refundable, many=True)
            total_expected=0
            total_one_off=0
            total_refund=0
            total_recurring=0
            for s in serial.data:
                total_expected=total_expected+s['amount']
            for se in serial_1.data:
                total_one_off=total_one_off+se['amount']
            for ser in serial_2.data:
                total_recurring=total_recurring+ser['amount']
            for seri in serial_3.data:
                total_refund=total_refund+seri['amount']
            
        
            

        return Response({
            "data":serial.data,
            "total_amount":total_expected,
            "one_off":total_one_off,
            "refundable":total_refund,
            "recurring":total_recurring
            
        })

class TenantDetails(APIView):
    permission_classes([IsAuthenticated])
    def get(self, request):
        print(request.user)

        tenant = Tenant.objects.get(user=request.user.id)
        user_info=UserSerializer(request.user)
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
        serializer_2.data.update({
            'email':user_info.data['email']
        })
        prop_id=serializer_2.data['property']
        flat_id=serializer_2.data['flat']
        prop_query=Property.objects.filter(id=prop_id).first()
        flat_query=Flat.objects.filter(id=flat_id).first()
        prop_serial=PropertySerializer(prop_query)
        flat_serial=FlatSerializer(flat_query)
        serializer_2.data.update({
            'property_name':prop_serial.data['property_name']
        })
        prop_name=prop_serial.data['property_name']
        return Response({
            'email':user_info.data['email'],
            'property_address':prop_serial.data['address'],
            'flat_name':flat_serial.data['name'],
            'data': serializer_2.data,
            'assigned_account': item,

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

class PaySalaryView(CreateAPIView):
    serializer_class = SalaryPaymentSerializer
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
    
class ViewSalary(APIView):
    def get(self, request):
        salary = PaySalary.objects.filter(manager=request.user)
        salary_paid = PaySalary.objects.filter(manager=request.user, manager_verify=True)
        salary_serializer=SalaryPaymentSerializer(salary, many=True)
        salary_paid_serializer=SalaryPaymentSerializer(salary_paid, many=True)
        total_income=0
        for sal in salary_paid_serializer.data:
            total_income=total_income+sal['amount']
        
            
        
        return Response({
            'salary_details':salary_serializer.data,
            'total_income':total_income        
        })

class LandlordViewSalary(APIView):
    def get(self, request,id):
        salary = PaySalary.objects.filter(manager=id)
        salary_paid = PaySalary.objects.filter(manager=id, manager_verify=True)
        salary_serializer=SalaryPaymentSerializer(salary, many=True)
        salary_paid_serializer=SalaryPaymentSerializer(salary_paid, many=True)
        total_income=0
        for sal in salary_paid_serializer.data:
            total_income=total_income+sal['amount']
        
            
        
        return Response({
            'salary_details':salary_serializer.data,
            'total_income':total_income        
        })
        
class ApproveSalary(UpdateAPIView):
    serializer_class = ApproveSalarySerializer
    permission_classes = [IsAuthenticated]
    model = PaySalary

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
            document = LandlordTenantDoc.objects.filter(tenant=id, user=request.user)
        except LandlordTenantDoc.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        if request.method == 'GET':
            serializer = LandlordTenantDocSerializer(document, many=True)
            return Response(serializer.data)

class LandlordManagerFiles(APIView):
    def get(self, request, id):
        try:
            document = LandlordDocument.objects.filter(manager=id, user=request.user)
        except LandlordDocument.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        if request.method == 'GET':
            serializer = LandlordDocumentSerializer(document, many=True)
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
            
class TenantPaymentView(APIView):
    def get(self, request):
        if request.method == 'GET':
            ten=request.user
            pay=MakePayment.objects.filter(tenant=ten)
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
        count_1= AddPayment.objects.filter(tenant=request.user.id, type="one-off")
        count_2= AddPayment.objects.filter(tenant=request.user.id, type="refundable")
        
        pay = MakePayment.objects.filter(tenant=request.user.id, status=True)
        pay_serializer = MakePaymentSerializer(pay, many=True)
        one_off = AddPaymentSerializer(count_1, many=True)
        optional_pay=AddPaymentSerializer(count_2,many=True)
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
            test="0"
        paid=0
        years=0
        one_off_total=0
        for amount in one_off.data:
            one_off_total=one_off_total+amount['amount']
        for pay in pay_serializer.data:
            paid=paid+pay["amount"]
        expected_pay=0
        optional_total=0
        one_off_total=0
        for pay in expected_rent.data:
            expected_pay=expected_pay+pay["amount"]
        for amount in optional_pay.data:
            optional_total=optional_total+amount['amount']
        for amount in one_off.data:
            one_off_total=one_off_total+amount['amount']
        if expected_pay !=0:
            
            if paid/expected_pay>=1:
                if paid/(expected_pay+one_off_total)>=1:
                    years=years+((((paid-one_off_total)//expected_pay)-1)*365)
        if paid>=expected_pay:
            pass
        #else:
        #test='0'
            
        if 's' in test:
            test =str(test.split("days")[0])
        else:
            test =str(test.split("day")[0])
            
        if test=="0:00:00":
            test="0"
        rent_status=""
        debt=0
        if paid>=expected_pay:
            rent_status="paid"
            debt=0

        else:
            debt=expected_pay-paid
            rent_status="owing"
        check=(int(test)+years)
        if check<0:
            value=(check//365)
            debt = value*expected_pay
            debt=(debt+paid-expected_pay)
            rent_status="owing"
        
        
            
        
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
             "days_left":(int(test)+years),
             "rent_status":rent_status,
             "debt":debt
             
             
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
                paid = MakePayment.objects.filter(property=data, status=True)
                tenant = Tenant.objects.filter(property=data)
                serial_2 = AddPaymentSerializer(payment, many=True)
                serial_3 = MakePaymentSerializer(paid, many=True)
                #
                tenant_prop=Tenant.objects.filter(id=data)
                #
                tenant_paid=0
                for t in serial_3.data:
                    tenant_paid = tenant_paid + t['amount']
                    i.update({'Sum':tenant_paid})
                sum =0
                for s in serial_2.data:
                    sum = sum + s['amount']
                    i.update({'paid':sum})
                
                expense = 0
                for s in serializer_2.data:
                    expense = expense + s['amount']
                i.update({'expenses':expense})
                if tenant_paid>sum:
                    debt=0
                else:
                    debt= tenant_paid-sum
                i.update({
                    "debt":debt,
                    "total_sum":tenant_paid   
                })
                a=i['user']
                m=0
                total_income=0
                if a!=None:
                    man=Manager.objects.filter(user=a).last()
                    m=man.user
                    salary_paid = PaySalary.objects.filter(manager=m, manager_verify=True)
                    salary_paid_serializer=SalaryPaymentSerializer(salary_paid, many=True)
                    for sal in salary_paid_serializer.data:
                        total_income=total_income+sal['amount']
                            
                    user_data=ManagerSerializer(man)
                    i.update({
                        "manager":user_data.data['first_name']+' '+user_data.data['last_name'],
                        "annual_salary":user_data.data['annual_salary'],
                        "phone-number":user_data.data['phone_number'],
                        "total_income":total_income
                    })
                else:
                    m=0
                    i.update({
                        "manager":None,
                        "annual_salary":None,
                        "phone-number":None,
                        "total_income":0
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
        
class EditFlatProp(CreateAPIView):
    serializer_class = EditFlatFromProp
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
            prop = serializer.save()
            print(prop)
            return Response({
                'message': "Flat Created and added successfully",
                'data': serializer.data
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)

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
        
class EditProperty(UpdateAPIView):
    serializer_class = EditPropertySerializer
    permission_classes = [IsAuthenticated]
    model = Flat

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
        
class AssignedAccList(APIView):
    def get(self, request):
        acc=AssignAccount.objects.all()
        acc_serial=AssignAccountSerializer(acc, many=True)
        for acc in acc_serial.data:
            prop_id=acc['property']
            acc_id=acc['id']
            prop=Property.objects.filter(id=prop_id).first()
            acc_data=AddAccount.objects.filter(id=acc_id).first()
            prop_serial=PropertySerializer(prop)
            account_serial=AddAccountserializer(acc_data)
            acc.update({
                "account_name":account_serial.data['account_name'],
                "bank_name":account_serial.data['bank_name'],
                "account_number":account_serial.data['account_number'],
                "property_name":prop_serial.data['property_name']
            })
            
        return Response(acc_serial.data)
        
class TestView(APIView):
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
            for s in serializer.data:
                data= s['id']
                head_id = s['user']
                expenses = AddExpenses.objects.filter(house=data)
                serializer_2 = AddExpensesserializer(expenses, many=True)
                expense = 0
                for seri in serializer_2.data:
                    expense = expense + seri['amount']
                s.update({'expenses':expense})
                total_debt=0
                total_paid=0
                total_expected=0
                flat_data=Flat.objects.filter(test_id=data, vacant=False)
                flat_serializer=FlatSerializer(flat_data, many=True)
                for i in flat_serializer.data:
                    testing=i['id']
                    tenant_data=Tenant.objects.filter(flat=testing).last()
                    ten=TenantSerializer(tenant_data)
                    tester=ten.data['user']
                    #somestuff

                    count_down= AddPayment.objects.filter(tenant=tester, type="recurring").last()
                    count= AddPayment.objects.filter(tenant=tester, type="recurring")
                    count_1= AddPayment.objects.filter(tenant=tester, type="recurring")
                    count_2= AddPayment.objects.filter(tenant=tester, type="refundable")
                    count_3= AddPayment.objects.filter(tenant=tester, type="one-off")
                    pay = MakePayment.objects.filter(tenant=tester, status=True)
                    pay_serializer = MakePaymentSerializer(pay, many=True)
                    serializer_data = AddPaymentSerializer(count_down)
                    expected_rent=AddPaymentSerializer(count,many=True)
                    optional_pay=AddPaymentSerializer(count_2,many=True)
                    one_off=AddPaymentSerializer(count_3,many=True)
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
                    optional_total=0
                    one_off_total=0
                    for amount in one_off.data:
                        one_off_total=one_off_total+amount['amount']
                    for pay in expected_rent.data:
                        expected_pay=expected_pay+pay["amount"]
                    for amount in optional_pay.data:
                        optional_total=optional_total+amount['amount']
                    if expected_pay!=0:
                        if paid/(expected_pay)>=1:
                            years=years+(((paid//(expected_pay))-1)*365)
                    if 's' in test:
                        test =str(test.split("days")[0])
                    else:
                        test =str(test.split("day")[0])
                        
                    if test=="0:00:00":
                        test="0"
                    if paid>=expected_pay:
                        debt=0
                    else:
                        #test='0'
                        debt=-(expected_pay-paid)
                    check=(int(test)+years)
                    if check<0:
                        value=(check//365)
                        debt = value*expected_pay
                        debt=(debt+paid-expected_pay)
                    elif check==0:
                        debt=-expected_pay
                    i.update({
                        "debt":debt
                    })
                        
                        
                    total_debt=total_debt+debt
                    total_paid=total_paid+paid
                    total_expected=total_expected+expected_pay
                s.update({
                    "debt":total_debt,
                    "Sum":total_paid,
                    "total_sum":total_expected
                })
                a=s['user']
                m=0
                total_income=0
                if a!=None:
                    man=Manager.objects.filter(user=a).last()
                    m=man.user
                    salary_paid = PaySalary.objects.filter(manager=m, manager_verify=True)
                    salary_paid_serializer=SalaryPaymentSerializer(salary_paid, many=True)
                    for sal in salary_paid_serializer.data:
                        total_income=total_income+sal['amount']
                            
                    user_data=ManagerSerializer(man)
                    s.update({
                        "manager":user_data.data['first_name']+' '+user_data.data['last_name'],
                        "annual_salary":user_data.data['annual_salary'],
                        "phone-number":user_data.data['phone_number'],
                        "total_income":total_income
                    })
                else:
                    m=0
                    s.update({
                        "manager":None,
                        "annual_salary":None,
                        "phone-number":None,
                        "total_income":0
                    })
        return Response({
            'data':serializer.data
            #'flat_data':flat_serializer.data
            
        })


        