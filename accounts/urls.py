from django.urls import path
from .api import RegisterApi
from .views import SignUp
urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('signup', SignUp.as_view()),
]