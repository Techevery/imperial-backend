from django.urls import path
from . import views
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RegisterAPI,LoginAPI

urlpatterns = [
    path('', views.index,name='index'),
    path('get-property/', views.get_property,name='get_property'),
    path('get-property/<int:id>', views.property_detail, name='property_detail'),
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/login/', views.LoginAPI.as_view(), name='login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('get-flat/', views.get_flat, name='get_flat'),
    path('get-flat/<int:id>', views.flat_detail,name='flat_detail'),
    path('get-manager/', views.get_manager, name='get_manager'),
    path('get-manager/<int:id>', views.manager_detail, name='manger_detail'),
    path('get-tenant/',views.get_tenant, name='get_tenant'),
    path('get-tenant/<int:id>', views.tenant_detail, name='tenant_detail')
    
]

urlpatterns = format_suffix_patterns(urlpatterns)