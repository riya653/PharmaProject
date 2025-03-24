from django.urls import path
from . import views

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
    path('submit-symptom-form/', views.submit_symptom_form, name='submit_symptom_form'),
    path('send-prescription/<int:form_id>/', views.send_prescription, name='send_prescription'),
    path('notifications/', views.notifications, name='notifications'),
]
