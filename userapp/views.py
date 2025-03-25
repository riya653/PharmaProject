from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Medicine, Appointment, CartDb, Order, RegisterDb,CheckoutDb
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from adminApp.models import MedicineDb
from django.http import JsonResponse
from DoctorApp.models import Notification,Appointment
import razorpay
from .forms import PatientAppointmentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
from DoctorApp.models import Notification

def home(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    return render(request, 'Home.html', {'cart_count': x})


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
    if request.method == "POST":
        un = request.POST.get('username')
        pswd = request.POST.get('pass')

        # Check from RegisterDb (custom DB)
        if RegisterDb.objects.filter(Username=un, Password=pswd).exists():
            request.session['Username'] = un
            messages.success(request, "Welcome to Pharma")
            return redirect(home)
        else:
            messages.warning(request, "Failed To Login")
            return redirect(sign_in)

    messages.warning(request, "Failed")
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
    username = request.session.get('Username')
    customer = CartDb.objects.filter(Username=username).order_by('-id').first()

    if not customer:
        return JsonResponse({'error': 'No items found in cart!'})

    pay = customer.Total_Price or 0
    amount = int(pay * 100)  # Amount in paise
    pay_str = str(amount)

    if request.method == "POST":
        try:
            # Razorpay client setup
            client = razorpay.Client(auth=('rzp_test_OeaKOOhKcsCdcn', 'NySeZajvZmcgsBhkRX5UrRF4'))

            # Create Razorpay order
            payment_order = client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': '1'  # Auto capture
            })

            return JsonResponse({
                "order_id": payment_order['id'],
                "amount": amount
            })
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, "Payment.html", {'username': username, 'customer': customer, 'pay_str': pay_str})


def about_page(request):
    cart = CartDb.objects.filter(Username=request.session.get('Username', ''))
    x = cart.count()
    return render(request,"About.html",{'x':x})



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientAppointmentForm

def book_appointment(request):
    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            # Create a notification for the doctor
            Notification.objects.create(
                notification_type='Appointment',
                message=f"New appointment request from {appointment.patient} on {appointment.date} at {appointment.time}.",
                is_read=False
            )

            messages.success(request, 'Appointment booked successfully!')
            return redirect('home')  # Redirect to home or desired page
    else:
        form = PatientAppointmentForm()
    return render(request, 'appointment.html', {'form': form})





