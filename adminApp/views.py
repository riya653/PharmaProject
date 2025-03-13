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


def add_pharmacist(request):
    return render(request,"AddPharmacist.html")

def save_pharmacist(request):
    if request.method=="POST":
        first_name=request.POST.get('fname')
        last_name= request.POST.get('lname')
        age= request.POST.get('age')
        gender= request.POST.get('gender')
        phone= request.POST.get('number')
        address= request.POST.get('address')
        email_id= request.POST.get('email')
        exp= request.POST.get('experience')
        qua= request.POST.get('qualification')
        obj=PharmacistDb(First_Name=first_name,Last_Name=last_name,Age=age,Gender=gender,
                     Phone_Number=phone,Address=address,Email_Id=email_id,Experience=exp,Qualification=qua)
        obj.save()
        return redirect(add_pharmacist)

def display_pharmacist(request):
    pharmacist=PharmacistDb.objects.all()
    return render(request,"DisplayPharmacist.html",{'pharmacist':pharmacist})

def edit_pharmacist(request,ph_id):
    pharmacist=PharmacistDb.objects.get(id=ph_id)
    return render(request,"EditPharmacist.html",{'pharmacist':pharmacist})

def delete_pharmacist(request,ph_id):
    pharmacist=PharmacistDb.objects.filter(id=ph_id)
    pharmacist.delete()
    return redirect(display_pharmacist)

def update_pharmacist(request,pha_id):
    if request.method=="POST":
        fi= request.POST.get('fname')
        la= request.POST.get('lname')
        ag= request.POST.get('age')
        ge= request.POST.get('gender')
        ph= request.POST.get('number')
        ad= request.POST.get('address')
        em= request.POST.get('email')
        ex= request.POST.get('experience')
        qu = request.POST.get('qualification')

        PharmacistDb.objects.filter(id=pha_id).update(First_Name=fi,Last_Name=la,Age=ag,Gender=ge,
                     Phone_Number=ph,Address=ad,Email_Id=em,Experience=ex,Qualification=qu)
        return redirect(display_pharmacist)

#****************************Receptionist****************************************

def add_receptionist(request):
    return render(request,"AddReceptionist.html")

def save_receptionist(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        age= request.POST.get('age')
        gender= request.POST.get('gender')
        phone_number= request.POST.get('number')
        address= request.POST.get('address')
        email_id= request.POST.get('email')
        username= request.POST.get('username')
        password= request.POST.get('password')
        status= request.POST.get('status')
        joining_date= request.POST.get('joining_date')
        exp= request.POST.get('experience')
        qua= request.POST.get('qualification')
        obj=ReceptionistDb(First_Name=first_name,Last_Name=last_name,Age=age,Gender=gender,Phone_Number=phone_number,
                         Address=address,Email_Id=email_id,Username=username,Password=password,Status=status,
                         Joining_Date=joining_date,Experience=exp,Qualification=qua)
        obj.save()
        return redirect(add_receptionist)

def display_receptionist(request):
    receptionist=ReceptionistDb.objects.all()
    return render(request,"DisplayReceptionist.html",{'receptionist':receptionist})

def edit_receptionist(request,r_id):
    receptionist=ReceptionistDb.objects.get(id=r_id)
    return render(request,"EditReceptionist.html",{'receptionist':receptionist})

def delete_receptionist(request,r_id):
    receptionist=ReceptionistDb.objects.filter(id=r_id)
    receptionist.delete()
    return redirect(display_receptionist)

def update_receptionist(request,re_id):
    if request.method=="POST":
        first = request.POST.get('first_name')
        last= request.POST.get('last_name')
        ag= request.POST.get('age')
        gen= request.POST.get('gender')
        phone= request.POST.get('number')
        addr= request.POST.get('address')
        email= request.POST.get('email')
        user= request.POST.get('username')
        pas= request.POST.get('password')
        sta= request.POST.get('status')
        joi= request.POST.get('joining_date')
        exp = request.POST.get('experience')
        qua = request.POST.get('qualification')

        ReceptionistDb.objects.filter(id=re_id).update(First_Name=first,Last_Name=last,Age=ag,Gender=gen,
                            Phone_Number=phone,Address=addr,Email_Id=email,Username=user,
                            Password=pas,Status=sta,Joining_Date=joi,Experience=exp,Qualification=qua)
        return redirect(display_receptionist)

#**********************************************************************************



#$***********************************************************************************
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


#*************************************************************88

# 2️⃣ Add Prescription Form View
def add_prescription(request):
    # Fetching users with specific roles (patients and doctors)
    patients = User.objects.filter(profile__role="patient")  # Ensure that 'profile' is used here if you have a Profile model
    doctors = User.objects.filter(profile__role="doctor")  # Fetching doctors
    return render(request, "AddPrescription.html", {'patients': patients, 'doctors': doctors})

# 3️⃣ Save Prescription View
def save_prescription(request):
    if request.method == "POST":
        # Fetch data from form submission
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        medicine_name = request.POST.get('medicine_name')
        dosage = request.POST.get('dosage')
        instructions = request.POST.get('instructions')

        # Get the patient and doctor objects based on the IDs passed in the form
        patient = get_object_or_404(User, id=patient_id, profile__role="patient")
        doctor = get_object_or_404(User, id=doctor_id, profile__role="doctor")

        # Create and save the Prescription object
        prescription = PrescriptionDb(
            patient=patient,
            doctor=doctor,
            medicine_name=medicine_name,
            dosage=dosage,
            instructions=instructions
        )
        prescription.save()

        # Redirect to display the saved prescriptions
        return redirect(display_prescription)

# 4️⃣ Display All Prescriptions
def display_prescription(request):
    prescriptions = PrescriptionDb.objects.all()
    return render(request, "DisplayPrescription.html", {'prescriptions': prescriptions})

# 5️⃣ Edit Prescription Form View
def edit_prescription(request, p_id):
    prescription = get_object_or_404(PrescriptionDb, id=p_id)
    patients = User.objects.filter(profile__role="patient")  # Fetch patients for the dropdown
    doctors = User.objects.filter(profile__role='doctor')  # Fetch doctors for the dropdown
    return render(request, "EditPrescription.html", {'prescription': prescription, 'patients': patients, 'doctors': doctors})

# 6️⃣ Update Prescription
def update_prescription(request, p_id):
    if request.method == "POST":
        # Get updated form data
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        medicine_name = request.POST.get('medicine_name')
        dosage = request.POST.get('dosage')
        instructions = request.POST.get('instructions')

        # Fetch patient and doctor objects based on form submission
        patient = get_object_or_404(User, id=patient_id, profile__role="patient")
        doctor = get_object_or_404(User, id=doctor_id, profile__role="doctor")

        # Update the PrescriptionDb entry
        PrescriptionDb.objects.filter(id=p_id).update(
            patient=patient,
            doctor=doctor,
            medicine_name=medicine_name,
            dosage=dosage,
            instructions=instructions
        )

        # Redirect to display the updated prescriptions
        return redirect(display_prescription)

# 7️⃣ Delete Prescription
def delete_prescription(request, p_id):
    prescription = get_object_or_404(PrescriptionDb, id=p_id)
    prescription.delete()
    return redirect(display_prescription)
