from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views
from .views import MyTokenObtainPairView, MyTokenObtainPairView2, MyTokenObtainPairView3, MyTokenObtainPairSerializer,show, add_property, PropertyCreateApi, CurrentUserView, managers_list, tenants_list, AddAccountCreateApi, AssignAccountCreateApi, AddExpensesCreateApi, AccountView, ExpensesView, ManagerProperty, AddDocumentCreateApi, LandlordDocumentCreateApi, LandlordTenantDocCreateApi, ManagerFiles, ManagerDocumentCreateApi, ManagerDocumentView,TenantMyFilesCreateApi, TenantDocument, TenantFiles, LandlordTenantFiles,LandlordTenantMyFiles, TenantPaymentUpdate, TenantDetails, MakePayment, ViewPayment, PageView

urlpatterns = [

    path('login/landlord', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/manager', MyTokenObtainPairView2.as_view(), name='token_obtain_pair2'),
    path('login/tenant', MyTokenObtainPairView3.as_view(), name='token_obtain_pair3'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('display', views.show, name='show'),
    path('add', views.add_property),
    path('all-properties', views.get_property),
    path('get-property/<int:id>', views.property_detail),
    path('get-property/<int:id>/flats', views.flat_detail),
    path('add-property', PropertyCreateApi.as_view(), name='add'),
    path('user-details', CurrentUserView.as_view(), name='user'),
    path('managers', views.managers_list),
    path('tenants', views.tenants_list),
    path('add-account', AddAccountCreateApi.as_view()),
    path('assign-account', AssignAccountCreateApi.as_view()),
    path('add-expenses', AddExpensesCreateApi.as_view()),
    path('account-list', AccountView.as_view()),
    path('expenses', ExpensesView.as_view()),
    path('manager-property', ManagerProperty.as_view()),
    path('tenant/add-document', AddDocumentCreateApi.as_view()),
    path('tenant/my-files', TenantDocument.as_view()),
    path('tenant-payment', TenantPaymentUpdate.as_view()),
    path('tenant/details', TenantDetails.as_view()),
    path('make-payment', MakePayment.as_view()),
    path('landlord/add-manager-doc', LandlordDocumentCreateApi.as_view()),
    path('manager-files', ManagerFiles.as_view()),
    path('manager/add-document', ManagerDocumentCreateApi.as_view()),
    path('landlord/add-tenant-doc', LandlordTenantDocCreateApi.as_view()),
    path('manager/my-files', ManagerDocumentView.as_view()),
    path('tenant/add-document', TenantMyFilesCreateApi.as_view()),
    path('tenant-files', TenantFiles.as_view()),
    path('landlord/tenant-files/<int:id>', LandlordTenantMyFiles.as_view()),
    path('view-payment', ViewPayment.as_view()),
    path('page', PageView.as_view())
    
]