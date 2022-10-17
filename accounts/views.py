from django.shortcuts import render
from .models import User
from .forms import CustomUserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .serializer import *
from django.core.mail import send_mail


from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView

# Create your views here.
class SignUp(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy('sample')
    template_name = 'registration/signup.html'

class LandlordCreateAPIView(CreateAPIView):
    serializer_class = LandlordCreateSerializer
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
            user = serializer.save()
            data = serializer.data
            
                
            print(user)
            return Response({
                'message': "Landlord Registration successful",
                'data': serializer.data
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)


class ManagerCreateAPIView(CreateAPIView):
    serializer_class = ManagerCreateSerializer
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
            user = serializer.save()
            email = data.get('email')
            password = (user['password'])
                
            send_mail(
                'Mperial Account',
                'Here are your login details, email: {femail}, password: {fpassword}'.format(femail=email, fpassword=password),
                'noreply@techevery.ng',
                [email],
                fail_silently=False,
)
            print(user)
            return Response({
                'message': "Manager Registration successful",
                'data': serializer.data
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)
        
        
class TenantCreateAPIView(CreateAPIView):
    serializer_class = TenantCreateSerializer
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
            user = serializer.save()
            email = data.get('email')
            password = (user['password'])
                
            send_mail(
                'Mperial Account',
                'Here are your login details, email: {femail}, password: {fpassword}'.format(femail=email, fpassword=password),
                'noreply@techevery.ng',
                [email],
                fail_silently=False,
)
            print(user)
            return Response({
                'message': "Manager Registration successful",
                'data': serializer.data,
                "password": raw_password,

            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)