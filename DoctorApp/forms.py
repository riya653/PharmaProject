from django import forms
from .models import Prescription,Appointment,SymptomForm
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicine', 'dosage', 'notes']
        widgets = {
            'medicine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter medicine name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dosage'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add additional notes'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time', 'reason']



class SymptomForm(forms.ModelForm):
    class Meta:
        model = SymptomForm
        fields = ['patient_name', 'symptoms']