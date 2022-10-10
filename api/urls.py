from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views
from .views import MyTokenObtainPairView, MyTokenObtainPairSerializer,show, add_property, PropertyCreateApi

urlpatterns = [

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('display', views.show, name='show'),
    path('add', views.add_property),
    path('all-properties', views.get_property),
    path('get-property/<int:id>', views.property_detail),
    path('get-property/<int:id>/flats', views.flat_detail),
    path('add-property', PropertyCreateApi.as_view(), name='add')

]