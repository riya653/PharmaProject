from django.contrib import admin
from .models import Doctor
from .models import Appointment
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name','specialization','phone','status']
    search_fields = ['name','specialization']

admin.site.register(Doctor,DoctorAdmin)

##now

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'time', 'reason', 'status')
    list_filter = ('status', 'date')