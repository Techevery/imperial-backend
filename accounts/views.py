from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .models import User
from .forms import CustomUserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .serializer import *
from django.core.mail import send_mail
from accounts.send_password import send_text
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView, UpdateAPIView
import requests
from datetime import datetime, timedelta

import json
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.
class SignUp(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy('sample')
    template_name = 'registration/signup.html'

class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'registration/login.html'
    #form_class = LoginForm
    #success_url = reverse_lazy('home-web')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Get the username and password from the form data
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Make a POST request to the API endpoint with the login credentials
        api_url = 'https://mperial.techevery.ng/api/login/landlord'
        api_response = requests.post(api_url, data={'email': username, 'password': password})

        if api_response.status_code == 200:
            # Save the access and refresh tokens to cookies
            data = api_response.json()
            access_token = data['access']
            refresh_token = data['refresh']
            expires = 86400  # Token expiry time in seconds (1 day)

            # Set cookies for access_token and refresh_token
            response.set_cookie('access_token', access_token, max_age=expires)
            response.set_cookie('refresh_token', refresh_token, max_age=expires)

        return response
    '''def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Invalid login credentials')
        return response
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})'''
    def form_invalid(self, form):
        response = super().form_invalid(form)
        form.errors.clear()
        form.add_error('username', 'Invalid email or password')
        return response
    def get_success_url(self):
        return reverse_lazy('home-web')
        
    







class CustomLogoutView(LogoutView):
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Delete the access and refresh tokens from the cookie
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
        
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
            phone_num= data.get('phone_number')
            password = (user['password'])
            name=data.get('first_name')
                
            send_mail(
                'Mperial Account',
                'Here are your login details, email: {femail}, password: {fpassword}'.format(femail=email, fpassword=password),
                'noreply@techevery.ng',
                [email],
                fail_silently=True,
)
            send_text(num=phone_num,
            text="Hello " +name +" , here is your Login Details; \n " + "email: " + email + " , password: " + password
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
            phone_num= data.get('phone_number')
            name=data.get('first_name')
                
            send_mail(
                'Mperial Account',
                'Here are your login details, email: {femail}, password: {fpassword}'.format(femail=email, fpassword=password),
                'noreply@techevery.ng',
                [email],
                fail_silently=True,
)
            send_text(num=phone_num,
            text="Hello " +name +" , here is your Login Details; \n " + "email: " + email + " , password: " + password
            )
            print(user)
            return Response({
                'message': "Tenant Registration successful",
                'data': serializer.data,
                "password": raw_password,

            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)
        

class UpdateTenantView(UpdateAPIView):
    serializer_class = TenantChangeSerializer
    permission_classes = [IsAuthenticated]
    model = Tenant

    def put(self, request):
        instance = self.model.objects.get(user=request.user)
        serialized_data = self.get_serializer(instance, data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)


    def patch(self, request):

        instance = self.model.objects.get(user=request.user)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)
        
class UpdateManagerView(UpdateAPIView):
    serializer_class = ManagerChangeSerializer
    permission_classes = [IsAuthenticated]
    model = Manager

    def put(self, request):
        instance = self.model.objects.get(user=request.user)
        serialized_data = self.get_serializer(instance, data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)


    def patch(self, request):

        instance = self.model.objects.get(user=request.user)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)
        
class UpdateLandlordView(UpdateAPIView):
    serializer_class = LandlordChangeSerializer
    permission_classes = [IsAuthenticated]
    model = LandLord

    def put(self, request):
        instance = self.model.objects.get(user=request.user)
        serialized_data = self.get_serializer(instance, data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)


    def patch(self, request):

        instance = self.model.objects.get(user=request.user)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)

class UpdateManagerPermission(UpdateAPIView):
    serializer_class = ManagerChangeSerializer
    permission_classes = [IsAuthenticated]
    model = Manager

    def put(self, request, id):
        instance = self.model.objects.get(user=id)
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

        instance = self.model.objects.get(user=id)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)

class DeactivateTenantView(UpdateAPIView):
    serializer_class = DeactivateTenantSerializer
    permission_classes = [IsAuthenticated]
    model = Tenant

    def put(self, request, id):
        instance = self.model.objects.get(user=id)
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

        instance = self.model.objects.get(user=id)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)
        
class DeactivateManagerView(UpdateAPIView):
    serializer_class = DeactivateManagerSerializer
    permission_classes = [IsAuthenticated]
    model = Manager

    def put(self, request, id, prop_id):
        instance = self.model.objects.get(user=id)
        serialized_data = self.get_serializer(instance, data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)


    def patch(self, request, id, prop_id):

        instance = self.model.objects.get(user=id)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)
        
class ReactivateTenantView(UpdateAPIView):
    serializer_class = ActivateTenantSerializer
    permission_classes = [IsAuthenticated]
    model = Tenant

    def put(self, request, id):
        instance = self.model.objects.get(user=id)
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

        instance = self.model.objects.get(user=id)
        serialized_data = self.get_serializer(instance, data=request.data, partial=True)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(serialized_data.data)

        error_keys = list(serialized_data.errors.keys())
        if error_keys:
            error_msg = serialized_data.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serialized_data.errors, status=400)
        
class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    