from django import forms
from DoctorApp.models import Appointment

class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time', 'reason']
        widgets = {
            'patient': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter reason for appointment'}),
        }
