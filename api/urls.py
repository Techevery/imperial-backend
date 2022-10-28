from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views
from .views import MyTokenObtainPairView, MyTokenObtainPairSerializer,show, add_property, PropertyCreateApi, CurrentUserView, managers_list, tenants_list, AddAccountCreateApi, AssignAccountCreateApi, AddExpensesCreateApi, AccountView, ExpensesView, ManagerProperty, AddDocumentCreateApi, TenantDocument, TenantPaymentUpdate

urlpatterns = [

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
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
    path('tenant-document', TenantDocument.as_view()),
    path('tenant-payment', TenantPaymentUpdate.as_view()),
    

]