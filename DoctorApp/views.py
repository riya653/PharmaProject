from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import authenticate, login
from adminApp.models import DoctorDb

def doctor_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)  # Check credentials
        if user is not None:
            try:
                doctor = DoctorDb.objects.get(user=user)  # Check if doctor exists
                login(request, user)
                return redirect('doctor_dashboard')  # Redirect to Doctor Dashboard
            except DoctorDb.DoesNotExist:
                return render(request, 'login.html', {'error': 'You are not registered as a doctor'})
        else:
            return render(request,'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')