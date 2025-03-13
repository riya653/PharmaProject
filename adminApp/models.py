from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class PatientDb(models.Model):
    First_Name=models.CharField(max_length=100,null=True,blank=True)
    Last_Name=models.CharField(max_length=100,null=True,blank=True)
    Age=models.IntegerField(null=True,blank=True)
    Gender=(models.CharField(max_length=100,null=True,blank=True))
    Phone_Number=models.IntegerField(null=True,blank=True)
    Blood_Group=models.CharField(max_length=20,null=True,blank=True)
    Address=models.CharField(max_length=100,null=True,blank=True)
    Email_Id=models.EmailField(max_length=100,null=True,blank=True)
    Emergency=models.IntegerField(null=True,blank=True)
    Date=models.CharField(max_length=100,null=True,blank=True)
    Profile_Image=models.ImageField(upload_to="Profile",null=True,blank=True)


class DoctorDb(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #!!!!!!!!!!!
    First_Name=models.CharField(max_length=100,null=True,blank=True)
    Last_Name=models.CharField(max_length=100,null=True,blank=True)
    Age=models.IntegerField(null=True,blank=True)
    Gender=(models.CharField(max_length=100,null=True,blank=True))
    Specialization=(models.CharField(max_length=100,null=True,blank=True))
    Phone_Number=models.IntegerField(null=True,blank=True)
    Address=models.CharField(max_length=100,null=True,blank=True)
    Email_Id=models.EmailField(max_length=100,null=True,blank=True)
    Experience=models.IntegerField(null=True,blank=True)


class PharmacistDb(models.Model):
    First_Name = models.CharField(max_length=100, null=True, blank=True)
    Last_Name = models.CharField(max_length=100, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    Gender = models.CharField(max_length=100, null=True, blank=True)
    Phone_Number = models.IntegerField(null=True, blank=True)
    Address = models.CharField(max_length=255, null=True, blank=True)
    Email_Id = models.EmailField(max_length=100, null=True, blank=True)
    Experience = models.IntegerField(null=True, blank=True)
    Qualification = models.CharField(max_length=100, null=True, blank=True)


class ReceptionistDb(models.Model):
    First_Name = models.CharField(max_length=100, null=True, blank=True)
    Last_Name = models.CharField(max_length=100, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    Gender = models.CharField(max_length=100, null=True, blank=True)
    Phone_Number = models.IntegerField( null=True, blank=True)
    Address = models.CharField(max_length=255, null=True, blank=True)
    Email_Id = models.EmailField(max_length=100, null=True, blank=True)
    Username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    Password = models.CharField(max_length=255, null=True, blank=True)
    Status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    Joining_Date = models.DateField(null=True, blank=True)
    Experience = models.IntegerField(null=True, blank=True)
    Qualification = models.CharField(max_length=100, null=True, blank=True)


# class MedicineCategoryDb(models.Model):
#     category_name = models.CharField(max_length=200, default="Unknown")
#     description = models.CharField(max_length=500, default="No description")
#     status = models.CharField(max_length=50, default="active")
#     created_at = models.DateTimeField(auto_now_add=True)  # Ensure this is 'created_at', not 'Created_at'
#     updated_at = models.DateTimeField(auto_now=True)


#*********************************************************
class MedicineDb(models.Model):
    Name = models.CharField(max_length=200,null=False,blank=False)
    price = models.IntegerField(null=True,blank=True)
    symptoms = models.TextField(default="No symptoms provided", help_text="Enter symptoms separated by commas")
    description = models.TextField()
    stock = models.IntegerField(default=0)
#***************************!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('pharmacist', 'Pharmacist'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')

class PrescriptionDb(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prescriptions")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_prescriptions")
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


