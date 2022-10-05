from django.shortcuts import render
from .models import User
from .forms import CustomUserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
class SignUp(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy('sample')
    template_name = 'registration/signup.html'
