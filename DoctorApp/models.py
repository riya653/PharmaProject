from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    address=models.TextField()
    status=models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    patient = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.patient} - {self.date}"




# Patient Symptom Form Model
class PatientForm(models.Model):
    patient_name = models.CharField(max_length=100)
    symptoms = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Reviewed', 'Reviewed')], default='Pending')

    def __str__(self):
        return self.patient_name


# Prescription Model
class Prescription(models.Model):
    patient_name = models.CharField(max_length=100)
    medicine = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    date_prescribed = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.patient_name}"


# DoctorApp/models.py
from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('Appointment', 'Appointment'),
        ('Form Submission', 'Form Submission'),
        ('Prescription', 'Prescription'),
    )

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} - {self.message}"



class SymptomForm(models.Model):
    patient_name = models.CharField(max_length=100)
    symptoms = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.date_submitted}"
