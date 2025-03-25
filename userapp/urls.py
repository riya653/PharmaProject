from django.urls import path
from userapp import views
urlpatterns=[
    path('home/', views.home, name="home"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('', views.sign_in, name="sign_in"),
    path('save_signup/', views.save_signup, name="save_signup"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('medicine_list/', views.medicine_list, name="medicine_list"),
    path('single_item/<int:item_id>',views.single_item,name="single_item"),
    path('symptom_checker/', views.symptom_checker, name="symptom_checker"),
    path('save_cart/',views.save_cart,name="save_cart"),
    path('cart_page/',views.cart_page,name="cart_page"),
    path('checkout/',views.checkout,name="checkout"),
    path('save_checkout/',views.save_checkout,name="save_checkout"),
    path('payment/',views.payment,name="payment"),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('about_page/', views.about_page, name='about_page'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),



]
