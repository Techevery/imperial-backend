from django.shortcuts import render, redirect, get_object_or_404
from api.models import Property, MakePayment, Flat
from accounts.models import  Manager, Tenant
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from api.models import Flat, Property
from .forms import PropertyForm, FlatForm



# Create your views here.
User = get_user_model()

def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            #property.user = request.user
            property.manager_vacant = False
            property.save()

            # Save selected flats
            selected_flats = request.POST.getlist('flats')
            property.flats.set(selected_flats)

            return redirect('property_list') # replace with the URL name of your property list view
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form, 'flat_form': FlatForm()})




def get_prop(request):
    prop_list_data =[]
    url = "https://mperial.techevery.ng/api/all-properties"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        prop_list_data=data[0:3]
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return{"data":prop_list_data}

def get_full_prop(request):
    prop_list_data =[]
    url = "https://mperial.techevery.ng/api/all-properties"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        prop_list_data=data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return{"data":prop_list_data}
    
#get property by id    
def get_one_prop(request, id):
    prop_list_data =[]
    url = f"https://mperial.techevery.ng/api/get-property/{id}"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        prop_list_data=data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return{"data":prop_list_data}


def get_manager_myfiles(request, id):
    files_data = []
    url = f"https://mperial.techevery.ng/api/landlord/manager-files/{id}"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        files_data = data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return {"data": files_data}
    
def get_manager_files(request, id):
    files_data = []
    url = f"https://mperial.techevery.ng/api/landlord/files/manager/{id}"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        files_data = data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return {"data": files_data}
    
def get_tenant_myfiles(request, id):
    full_files_data = []
    url = f"https://mperial.techevery.ng/api/landlord/tenant-files/{id}"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        full_files_data = data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
        
    paginator = Paginator(full_files_data, 3)  # 10 items per page
    page_number = request.GET.get('page')
    files_data = paginator.get_page(page_number)
    return {"data": files_data}
    
def get_tenant_files(request, id):
    full_files_data = []
    url = f"https://mperial.techevery.ng/api/landlord/files/tenant/{id}"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        full_files_data = data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    paginator = Paginator(full_files_data, 3)  # 10 items per page
    page_number = request.GET.get('page')
    files_data = paginator.get_page(page_number)
    return {"data": files_data}

@login_required
def get_manager(request):
    manager_list_data =[]
    url = "https://mperial.techevery.ng/api/managers"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        manager_list_data=data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return{"data":manager_list_data}
    
@login_required
def get_tenant(request):
    tenant_list_data =[]
    url = "https://mperial.techevery.ng/api/tenants"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        tenant_list_data=data
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return{"data":tenant_list_data}

@login_required
def home(request):
    prop_data = get_prop(request)
    property_count = Property.objects.count()
    manager_count = Manager.objects.count()
    tenant_count = Tenant.objects.count()
    context_data={}
    context_data.update({'property_list':prop_data['data']})
    context_data.update({'property':property_count, 'manager':manager_count, 'tenant':tenant_count})
    url = "https://mperial.techevery.ng/api/landlord/profile"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        context_data.update({'response':data})
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    url = "https://mperial.techevery.ng/api/landlord/profile"
    access_token = request.COOKIES.get('access_token')
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        data = response.json()
        context_data.update({'response':data})
    else:
        # Error: handle the response error
        print(f"Error {response.status_code}: {response.text}")
    return render(request, "home.html", context_data)
    
@login_required
def manager_web(request):
    manager_list = Manager.objects.all()
    manager_data = get_manager(request)
    context_data={}
    context_data.update({'manager_list':manager_data['data'], 'man_list':manager_list})
    return render(request, "tables.html", context_data)
    
    
@login_required
def tenant_web(request):
    tenant_list = Tenant.objects.all()
    tenant_data = get_tenant(request)
    context_data={}
    context_data.update({'tenant_list':tenant_data['data'], 'ten_list':tenant_list})
    return render(request, "tenants_list.html", context_data)

@login_required
def property_web(request):
    prop_data = get_full_prop(request)
    context_data={}
    context_data.update({'property_list':prop_data['data']})
    return render(request, "properties.html", context_data)

@login_required
def payments_web(request):
    payment_data = MakePayment.objects.all()
    context_data = {"payments":payment_data}
    return render(request, "payments.html", context_data)

@login_required
def analytics_web(request):
    return render(request, "analytics.html")

@login_required
def manager_detail_web(request, id):
    param = id
    man = User.objects.get(id=id)
    manager_data = Manager.objects.get(user=man)
    prop_count = Property.objects.filter(user=man).count()
    property_data = Property.objects.filter(user=man)
    file_data = get_manager_myfiles(request, param)
    file_data_2 = get_manager_files(request, param)
    context_data={}
    context_data.update({'myfiles':file_data['data'], 'myfiles_2':file_data_2['data'], 'property_count':prop_count, 'property':property_data, 'manager':manager_data})
    return render(request, "billing.html", context_data)

@login_required
def tenant_detail_web(request, id):
    param = id
    ten = User.objects.get(id=id)
    tenant_data = Tenant.objects.get(user=ten)
    file_data = get_tenant_myfiles(request, param)
    file_data_2 = get_tenant_files(request, param)
    context_data={}
    context_data.update({'myfiles':file_data['data'], 'myfiles_2':file_data_2['data'],'tenant':tenant_data})
    return render(request, "tenant_detail.html", context_data)

@login_required
def property_detail_web(request, id):
    param = id
    prop_data= Property.objects.get(id=id)
    flat_users = Tenant.objects.filter(property=prop_data)
    prop_user = prop_data.user
    manager = prop_user.manager
    prop = get_one_prop(request, param)
    context_data={"property":prop_data, "manager":manager, "props":prop['data'],"flat_users":flat_users}
    return render(request, "property_detail.html", context_data)

def prop_info(request):
    return render(request, "property_info.html")
    

def flat_create(request, id):
    property = get_object_or_404(Property, id=id)
    param = id

    if request.method == 'POST':
        form = FlatForm(request.POST)
        if form.is_valid():
            flat = form.save(commit=False)
            flat.test_id = param
            flat.save()
            property.flats.add(flat)  # Add the created flat to the property's flat field
            return redirect('property-detail', id=param)  # Replace 'home-web' with the desired URL name or path to redirect after successful form submission
    else:
        form = FlatForm()
    
    return render(request, 'flat_create.html', {'form': form})
    

    
