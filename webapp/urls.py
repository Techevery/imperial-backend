from . import views
from django.urls import path


urlpatterns =[
    path('', views.home, name="home-web"),
    path('manager/web', views.manager_web, name='manager-web'),
    path('tenant/web', views.tenant_web, name='tenant-web'),
    path('analytics', views.analytics_web, name='analytics'),
    path('manager/detail/web/<int:id>', views.manager_detail_web, name='manager-detail'),
    path('tenant/detail/web/<int:id>', views.tenant_detail_web, name='tenant-detail-web'),
    path('property/detail/<int:id>', views.property_detail_web, name='property-detail'),
    path('flat/add/<int:id>', views.flat_create, name='add_flat'),
    path('property/web', views.property_web, name='property-web'),
    path('property/info', views.prop_info, name='prop-info'),
    path('payment/web', views.payments_web, name='payment-web'),
    path('add-property', views.add_property, name='add-property')
    ]
