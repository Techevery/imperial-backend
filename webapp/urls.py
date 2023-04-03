from . import views
from django.urls import path


urlpatterns =[
    path('home', views.home, name="home-web"),
    path('manager/web', views.manager_web, name='manager-web'),
    path('tenant/web', views.tenant_web, name='tenant-web'),
    path('analytics', views.analytics_web, name='analytics'),
    path('manager/detail/web', views.manager_detail_web, name='manager-detail-web'),
    path('tenant/detail/web', views.tenant_detail_web, name='tenant-detail-web'),
    path('property/detail/web', views.property_detail_web, name='property-detail-web'),
    path('property/web', views.property_web, name='property-web'),
    path('payment/web', views.payments_web, name='payment-web'),
    ]
