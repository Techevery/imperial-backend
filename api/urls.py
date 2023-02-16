from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views
from .views import MyTokenObtainPairView, MyTokenObtainPairView2, MyTokenObtainPairView3, MyTokenObtainPairSerializer,show, add_property, PropertyCreateApi,EditProperty,EditFlatProp, CurrentUserView, managers_list,UserManager,UserLandlord, TenantList, tenants_list_manager, AddAccountCreateApi, AssignAccountCreateApi, AddExpensesCreateApi, AccountView, ExpensesView,ExpensesFlatView,ManagerExpensesView, ManagerProperty, AddDocumentCreateApi, LandlordDocumentCreateApi, LandlordTenantDocCreateApi, ManagerFiles, ManagerDocumentCreateApi, ManagerDocumentView,TenantMyFilesCreateApi, TenantDocument, TenantFiles,TenantDocdelete, LandlordTenantFiles,LandlordTenantMyFiles,LandlordManagerMyFiles,LandlordManagerFiles, TenantPaymentUpdate, TenantDetails,TenantPaymentView, MakePaymentView,PaySalaryView,ViewSalary,LandlordViewSalary,ApproveSalary, ViewPayment,ViewTenantPayment, PageView, ManagerProp, LandlordProperty,ApprovePayment, AllProperties, TenantViewLandlord, AssignedAccList, TestView

urlpatterns = [

        path('login/landlord', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/manager', MyTokenObtainPairView2.as_view(), name='token_obtain_pair2'),
    path('login/tenant', MyTokenObtainPairView3.as_view(), name='token_obtain_pair3'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('display', views.show, name='show'),
    path('add', views.add_property),
    path('all-properties', AllProperties.as_view()),
    path('edit-property/<int:id>', EditProperty.as_view()),
    path('edit-flat-property/<int:id>', EditFlatProp.as_view()),
    path('get-property/<int:id>', views.property_detail),
    path('get-property/<int:id>/flats', views.flat_detail),
    path('add-property', PropertyCreateApi.as_view(), name='add'),
    path('user-details', CurrentUserView.as_view(), name='user'),
    path('managers', views.managers_list),
    path('manager',UserManager.as_view()),
    path('landlord/profile',UserLandlord.as_view()),
    path('tenants', TenantList.as_view()),
    path('tenants/manager', views.tenants_list_manager),
    path('tenant/manager', TenantViewLandlord.as_view()),
    path('add-account', AddAccountCreateApi.as_view()),
    path('assign-account', AssignAccountCreateApi.as_view()),
    path('add-expenses', AddExpensesCreateApi.as_view()),
    path('account-list', AccountView.as_view()),
    path('expenses', ExpensesView.as_view()),
    path('expenses/flat/<int:id>',ExpensesFlatView.as_view()),
    path('expenses/manager/<int:id>',ManagerExpensesView.as_view()),
    path('manager-property/<int:id>', ManagerProperty.as_view()),
    path('tenant/add-document', AddDocumentCreateApi.as_view()),
    path('tenant/my-files', TenantDocument.as_view()),
    path('tenant-myfiles/delete/<int:id>', TenantDocdelete.as_view()),
    path('tenant-payment', TenantPaymentUpdate.as_view()),
    path('tenant/details', TenantDetails.as_view()),
    path('make-payment', MakePaymentView.as_view()),
    path('pay-salary', PaySalaryView.as_view()),
    path('manager/salary-payments', ViewSalary.as_view()),
    path('landlord/salary-payments/<int:id>', LandlordViewSalary.as_view()),
    path('approve-salary/payment/<int:id>', ApproveSalary.as_view()),
    path('landlord/add-manager-doc', LandlordDocumentCreateApi.as_view()),
    path('manager-files', ManagerFiles.as_view()),
    path('manager/add-document', ManagerDocumentCreateApi.as_view()),
    path('landlord/add-tenant-doc', LandlordTenantDocCreateApi.as_view()),
    path('manager/my-files', ManagerDocumentView.as_view()),
    path('tenant/add-document', TenantMyFilesCreateApi.as_view()),
    path('tenant-files', TenantFiles.as_view()),
    path('landlord/tenant-files/<int:id>', LandlordTenantMyFiles.as_view()),
    path('landlord/manager-files/<int:id>', LandlordManagerMyFiles.as_view()),
    path('landlord/files/manager/<int:id>', LandlordManagerFiles.as_view()),
    path('landlord/files/tenant/<int:id>', LandlordTenantFiles.as_view()),
    path('tenant/view-payment', TenantPaymentView.as_view()),
    path('view-payment', ViewPayment.as_view()),
    path('view-payment/<int:id>', ViewTenantPayment.as_view()),
    path('page', PageView.as_view()),
    path('manager-prop', TestView.as_view()),
    path('landlord-property/<int:id>', LandlordProperty.as_view()),
    path('approve-payment/<int:id>', ApprovePayment.as_view()),
    path('assigned/accounts', AssignedAccList.as_view()),
    path('test', TestView.as_view())
]