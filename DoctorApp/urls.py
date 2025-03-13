from django.urls import path
from .views import doctor_login

urlpatterns = [
    path('login/', doctor_login, name='doctor_login'),
]