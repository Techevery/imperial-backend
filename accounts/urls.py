from django.urls import path
from .api import RegisterApi
from .views import SignUp, LandlordCreateAPIView, ManagerCreateAPIView, TenantCreateAPIView, UpdateTenantView, UpdateManagerView, UpdateLandlordView, UpdateManagerPermission, DeactivateTenantView,ReactivateTenantView,DeactivateManagerView, ChangePasswordView

urlpatterns = [
      
      path('api/register', RegisterApi.as_view()),
      path('signup', SignUp.as_view()),
      path('landlord_register', LandlordCreateAPIView.as_view(), name='landlord_register'),
      path('manager_register', ManagerCreateAPIView.as_view(), name='manager_register'),
      path('tenant_register', TenantCreateAPIView.as_view(), name='manager_register'),
      path('update-tenant', UpdateTenantView.as_view()),
      path('update-manager', UpdateManagerView.as_view()),
      path('update-landlord', UpdateLandlordView.as_view()),
      path('approve-manager/<int:id>', UpdateManagerPermission.as_view()),
      path('deactivate-tenant/<int:id>', DeactivateTenantView.as_view()),
      path('reactivate-tenant/<int:id>', ReactivateTenantView.as_view()),
      path('deactivate-manager/<int:id>/prop/<int:prop_id>', DeactivateManagerView.as_view()),
      path('change-password', ChangePasswordView.as_view(), name='change-password')
]
