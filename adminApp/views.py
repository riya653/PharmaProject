from django.shortcuts import render,redirect, get_object_or_404
from adminApp.models import PatientDb, DoctorDb, PharmacistDb, ReceptionistDb,MedicineDb
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import PrescriptionDb
from django.conf import settings


# Create your views here.

def index_page(request):
    return render(request,"index.html")

def add_patient(request):
    return render(request,"AddPatient.html")

def save_patient(request):
    if request.method=="POST":
        first_name=request.POST.get('fname')
        last_name= request.POST.get('lname')
        age= request.POST.get('age')
        gender= request.POST.get('gender')
        phone_number= request.POST.get('number')
        blood= request.POST.get('blood')
        address= request.POST.get('address')
        email_id= request.POST.get('email')
        emergency= request.POST.get('emergency')
        doa= request.POST.get('doa')
        profile_image=request.FILES['profile']
        obj=PatientDb(First_Name=first_name,Last_Name=last_name,Age=age,Gender=gender,Phone_Number=phone_number,
                      Blood_Group=blood,Address=address,Email_Id=email_id,Emergency=emergency,
                      Date=doa,Profile_Image=profile_image)
        obj.save()
        return redirect(add_patient)

def display_patient(request):
    patient=PatientDb.objects.all()
    return render(request,"DisplayPatient.html",{'patient':patient})

def edit_patient(request,p_id):
    patient=PatientDb.objects.get(id=p_id)
    return render(request,"EditPatient.html",{'patient':patient})

def delete_patient(request,p_id):
    patient=PatientDb.objects.filter(id=p_id)
    patient.delete()
    return redirect(display_patient)

def update_patient(request,pa_id):
    if request.method=="POST":
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        ag= request.POST.get('age')
        gen= request.POST.get('gender')
        phone= request.POST.get('number')
        bloo= request.POST.get('blood')
        addr= request.POST.get('address')
        em= request.POST.get('email')
        emer= request.POST.get('emergency')
        do= request.POST.get('doa')
        try:
            img=request.FILES['profile']
            fs = FileSystemStorage()
            file= fs.save(img.name,img)
        except MultiValueDictKeyError:
            file=PatientDb.objects.get(id=pa_id).Profile_Image

        PatientDb.objects.filter(id=pa_id).update(First_Name=f_name,Last_Name=l_name,Age=ag,Gender=gen,
                                                  Phone_Number=phone,Blood_Group=bloo,
                                                  Address=addr,Email_Id=em,Emergency=emer,
                                                  Date=do,Profile_Image=file)
        return redirect(display_patient)

# Doctor

def add_doctor(request):
    return render(request,"AddDoctor.html")

def save_doctor(request):
    if request.method=="POST":
        first_name=request.POST.get('fname')
        last_name= request.POST.get('lname')
        age= request.POST.get('age')
        gender= request.POST.get('gender')
        spec= request.POST.get('special')
        phone= request.POST.get('number')
        address= request.POST.get('address')
        email_id= request.POST.get('email')
        exp= request.POST.get('experience')
        password = "doctor@123"  # Default password (can be changed later)
        user = User.objects.create_user(username=email_id, email=email_id, password=password)
        obj=DoctorDb(user=user, First_Name=first_name,Last_Name=last_name,Age=age,Gender=gender,
                     Specialization=spec,Phone_Number=phone,Address=address,Email_Id=email_id,Experience=exp)
        obj.save()
        return redirect(add_doctor)

def display_doctor(request):
    doctor=DoctorDb.objects.all()
    return render(request,"DisplayDoctor.html",{'doctor':doctor})

def edit_doctor(request,d_id):
    doctor=DoctorDb.objects.get(id=d_id)
    return render(request,"EditDoctor.html",{'doctor':doctor})

def delete_doctor(request,d_id):
    doctor=DoctorDb.objects.filter(id=d_id)
    doctor.delete()
    return redirect(display_doctor)

def update_doctor(request,do_id):
    if request.method=="POST":
        first= request.POST.get('fname')
        last= request.POST.get('lname')
        ag= request.POST.get('age')
        ge= request.POST.get('gender')
        spe= request.POST.get('special')
        pho= request.POST.get('number')
        addr= request.POST.get('address')
        email= request.POST.get('email')
        expe= request.POST.get('experience')

        DoctorDb.objects.filter(id=do_id).update(First_Name=first,Last_Name=last,Age=ag,Gender=ge,
                     Specialization=spe,Phone_Number=pho,Address=addr,Email_Id=email,Experience=expe)
        return redirect(display_doctor)


def add_medicine(request):
    return render(request,"AddMedicine.html")

def save_medicine(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = float(request.POST.get('price'))
        symptoms = request.POST.get('symptoms')
        description = request.POST.get('description')
        stock = int(request.POST.get('stock'))
        obj = MedicineDb(Name=name,price=price,symptoms=symptoms,description=description,stock=stock)
        obj.save()
        return redirect(add_medicine)


def display_medicine(request):
    medicines = MedicineDb.objects.all()
    return render(request, "DisplayMedicine.html", {'medicines': medicines})


def edit_medicine(request, m_id):
    medicine = MedicineDb.objects.get(id=m_id) # Fetch categories for dropdown
    return render(request, "EditMedicine.html", {'medicine': medicine})


def delete_medicine(request, m_id):
    medicine = MedicineDb.objects.get(id=m_id)
    medicine.delete()
    return redirect(display_medicine)


def update_medicine(request, m_id):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        symptoms = request.POST.get('symptoms')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        MedicineDb.objects.filter(id=m_id).update(Name=name,price=price,symptoms=symptoms,stock=stock,description=description)
        return redirect(display_medicine)


