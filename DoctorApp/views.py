from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Doctor
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from .models import PatientForm, Prescription
from .models import Notification
from .forms import AppointmentForm
from .models import SymptomForm as SymptomModel, Notification
from .forms import SymptomForm

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                doctor = Doctor.objects.get(user=user)
                login(request, user)
                return redirect('doctor_dashboard')
            except Doctor.DoesNotExist:
                return render(request, 'login.html', {'error': 'You are not authorized to access the doctor dashboard.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    return render(request, 'dashboard.html', {'doctor': doctor})


def doctor_logout(request):
    logout(request)
    return redirect('doctor_login')

# View to List Appointments
def view_appointments(request):
    appointments = Appointment.objects.all().order_by('-date')
    return render(request, 'appointments.html', {'appointments': appointments})

# Accept Appointment
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Accepted'
    appointment.save()
    return redirect('view_appointments')

# Reject Appointment
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Rejected'
    appointment.save()
    return redirect('view_appointments')

# View Patient Forms
def patient_forms(request):
    patient_forms = PatientForm.objects.all().order_by('-date_submitted')
    return render(request, 'patient_forms.html', {'patient_forms': patient_forms})

# Review Form & Send Prescription
def review_form(request, form_id):
    form = get_object_or_404(PatientForm, id=form_id)

    if request.method == 'POST':
        prescription = request.POST.get('prescription')
        Prescription.objects.create(
            patient=form.patient,
            prescription_text=prescription
        )
        form.is_reviewed = True
        form.save()
        return redirect('patient_forms')

    return render(request, 'review_form.html', {'form': form})



# View Prescriptions


def prescriptions(request):
    pending_forms = PatientForm.objects.filter(status='Reviewed')
    prescriptions = Prescription.objects.all().order_by('-date_prescribed')

    return render(request, 'prescriptions.html', {
        'pending_forms': pending_forms,
        'prescriptions': prescriptions
    })

from .models import Notification

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()

            # Create notification for new appointment
            Notification.objects.create(
                notification_type='Appointment',
                message=f"New appointment request from {form.cleaned_data['patient_name']}"
            )
            return redirect('view_appointments')



def submit_symptom_form(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            form.save()

            # Create notification for new symptom form submission
            Notification.objects.create(
                notification_type='Form Submission',
                message=f"New symptom form submitted by {form.cleaned_data['patient_name']}"
            )
            return redirect('home')
    else:
        form = SymptomForm()

    return render(request, 'submit_form.html', {'form': form})




def send_prescription(request, form_id):
    form = get_object_or_404(PatientForm, id=form_id)

    if request.method == 'POST':
        medicine = request.POST.get('medicine')
        dosage = request.POST.get('dosage')
        notes = request.POST.get('notes')

        Prescription.objects.create(
            patient_name=form.patient_name,
            medicine=medicine,
            dosage=dosage,
            notes=notes
        )

        # Update form status to Reviewed
        form.status = 'Reviewed'
        form.save()

        # Create notification for sent prescription
        Notification.objects.create(
            notification_type='Prescription',
            message=f"Prescription sent to {form.patient_name}"
        )

        return redirect('prescriptions')

    return render(request, 'send_prescription.html', {'form': form})

def notifications(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})
