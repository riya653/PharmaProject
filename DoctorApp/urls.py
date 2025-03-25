from django.urls import path
from DoctorApp import views

urlpatterns = [
    path('login/', views.doctor_login, name='doctor_login'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('logout/', views.doctor_logout, name='doctor_logout'),
    path('appointments/', views.view_appointments, name='view_appointments'),
    path('accept_appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('reject_appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('patient-forms/', views.patient_forms, name='patient_forms'),
    path('review-form/<int:form_id>/', views.review_form, name='review_form'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('notifications/', views.notifications, name='notifications'),

]
