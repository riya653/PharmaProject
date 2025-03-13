from django.shortcuts import render, redirect
from .models import Patient, Medicine, Appointment, CartDb, Order, RegisterDb,CheckoutDb
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from adminApp.models import MedicineDb
import razorpay
# Create your views here.
def home(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    return render(request,"Home.html",{'x':x})

def sign_in(request):
    return render(request,"patient_login.html")

def sign_up(request):
    return render(request,"patient_register.html")

def save_signup(request):
    if request.method=="POST":
        user=request.POST.get('username')
        psd=request.POST.get('pass1')
        con_psd=request.POST.get('pass2')
        em=request.POST.get('email')
        obj=RegisterDb(Username=user,Password=psd,Confirm_Password=con_psd,Email_Id=em)
        obj.save()
        messages.success(request,"Registered Successfully")
    return redirect(sign_in)

def user_login(request):
    if request.method=="POST":
        un=request.POST.get('username')
        pswd=request.POST.get('pass')
        if RegisterDb.objects.filter(Username=un,Password=pswd).exists():
            request.session['Username']=un
            request.session['Password']=pswd
            messages.success(request,"Welcome to Pharma")
            return redirect(home)
        else:
            messages.warning(request,"Failed To Login")
            return redirect(sign_in)
    else:
        messages.warning(request,"Failed")
        return redirect(sign_in)

def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(user_login)


# View Available Medicines
def medicine_list(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    medicines = MedicineDb.objects.all()
    return render(request,'medicine_list.html',{'medicines': medicines,'x':x})


def single_item(request,item_id):
    medicine=MedicineDb.objects.get(id=item_id)
    cart_count = CartDb.objects.filter(Username=request.session['Username'])
    x = cart_count.count()
    return render(request,"Single_Item.html",{'medicine':medicine,'x':x})



# Symptom Checker
def symptom_checker(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    all_symptoms=MedicineDb.objects.values_list('symptoms',flat=True)
    symptom_list=set()
    for symptom_str in all_symptoms:
        symptom_list.update(symptom_str.split(','))
    selected_medicines=None
    if request.method == "POST":
        selected_symptom = request.POST.get('symptom')
        selected_medicines=MedicineDb.objects.filter(symptoms__icontains=selected_symptom)

    return render(request, 'symptom_checker.html', {'symptoms': sorted(symptom_list),'medicines':selected_medicines,'x':x})



def book_appointment(request):
    if request.method == "POST":
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')

        try:
            doctor = User.objects.get(id=doctor_id)
            patient = Patient.objects.get(user=request.user)
            Appointment.objects.create(patient=patient, doctor=doctor, date=date, time=time, status="Pending")
            messages.success(request, "Appointment booked successfully")
            return redirect('appointment_history')
        except (User.DoesNotExist, Patient.DoesNotExist):
            messages.error(request, "Invalid Doctor or Patient")
            return redirect('book_appointment')

    return render(request, 'book_appointment.html')



# View Appointments
def appointment_history(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request,'appointment_history.html',{'appointments': appointments})


def save_cart(request):
    if request.method=="POST":
        user_name=request.POST.get('username')
        productname=request.POST.get('prod_name')
        quan=request.POST.get('quantity')
        pr=request.POST.get('price')
        to=request.POST.get('total')
        try:
            x= MedicineDb.objects.get(Name=productname)
        except MedicineDb.DoesNotExist:
            img=None
        obj=CartDb(Username=user_name,Medicine_Name=productname,Quantity=quan,Price=pr,Total_Price=to)
        obj.save()
        return redirect(home)


def cart_page(request):
    sub_total = 0
    shipping_amount = 0
    total_amount = 0
    x = 0
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    for i in cart:
        sub_total += i.Total_Price
        if sub_total > 500:
            shipping_amount = 50
        else:
            shipping_amount = 100
        total_amount = sub_total + shipping_amount
    x = cart.count()

    return render(request, "Cart.html", {
        'cart': cart,
        'sub_total': sub_total,
        'shipping_amount': shipping_amount,
        'total_amount': total_amount,
        'x': x
    })


def remove_from_cart(request,item_id):
    cart_item = CartDb.objects.get(id=item_id)
    cart_item.delete()  # Remove the cart item
    return redirect(cart_page)  # Redirect back to the cart page



def checkout(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    sub_total = 0
    shipping_amount = 0
    total_amount = 0
    cart_count = CartDb.objects.filter(Username=request.session['Username'])
    x = cart_count.count()
    cart = CartDb.objects.filter(Username=request.session['Username'])
    for i in cart:
        sub_total += i.Total_Price
        if sub_total > 500:
            shipping_amount = 50
        else:
            shipping_amount = 100
        total_amount = sub_total + shipping_amount
    return render(request,"checkout.html",{'cart':cart,'sub_total':sub_total,
                                       'shipping_amount':shipping_amount,'total_amount':total_amount,'x':x})

def save_checkout(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email = request.POST.get('email')
        place=request.POST.get('place')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        total=request.POST.get('total')
        message=request.POST.get('message')
        obj=CheckoutDb(Name=name,Email=email,Place=place,Address=address,State=state,
                       Mobile_Number=mobile,Pincode=pincode,Total_Price=total,Message=message)
        obj.save()
        return redirect(payment)

def payment(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    username = request.session.get('Username')
    customer = CartDb.objects.order_by('-id').first()
    pay = customer.Total_Price
    amount = int(pay * 100)  # Razorpay accepts amount in paise
    pay_str = str(amount)

    if request.method == "POST":
        client = razorpay.Client(auth=('rzp_test_OeaKOOhKcsCdcn', 'NySeZajvZmcgsBhkRX5UrRF4'))
        payment = client.order.create({'amount': amount, 'currency': 'INR'})  # FIXED: 'currency' instead of 'order_currency'

    return render(request, "Payment.html", {'username': username, 'customer': customer, 'pay_str': pay_str, 'x': x})


def about_page(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    return render(request,"About.html",{'x':x})

