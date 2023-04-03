from django.shortcuts import render
import requests

# Create your views here.

def home(request):
    response = requests.get('https://mperial.techevery.ng/api/user-details')
    return render(request, "home.html", {'response':response})

def manager_web(request):
    return render(request, "tables.html")

def tenant_web(request):
    return render(request, "tenants_list.html")

def property_web(request):
    return render(request, "properties.html")

def payments_web(request):
    return render(request, "payments.html")

def analytics_web(request):
    return render(request, "analytics.html")

def manager_detail_web(request):
    return render(request, "billing.html")

def tenant_detail_web(request):
    return render(request, "tenant_detail.html")

def property_detail_web(request):
    return render(request, "property_detail.html")
