from django.urls import path
from adminApp import views
urlpatterns=[
    path('index_page/',views.index_page,name="index_page"),
    path('add_patient/',views.add_patient,name="add_patient"),
    path('save_patient/',views.save_patient,name="save_patient"),
    path('display_patient/',views.display_patient,name="display_patient"),
    path('edit_patient/<int:p_id>/',views.edit_patient,name="edit_patient"),
    path('delete_patient/<int:p_id>/',views.delete_patient,name="delete_patient"),
    path('update_patient/<int:pa_id>/',views.update_patient,name="update_patient"),
    path('add_doctor/',views.add_doctor,name="add_doctor"),
    path('save_doctor/',views.save_doctor,name="save_doctor"),
    path('display_doctor/',views.display_doctor,name="display_doctor"),
    path('edit_doctor/<int:d_id>/',views.edit_doctor,name="edit_doctor"),
    path('delete_doctor/<int:d_id>/',views.delete_doctor,name="delete_doctor"),
    path('update_doctor/<int:do_id>/',views.update_doctor,name="update_doctor"),
    path('add_medicine/', views.add_medicine, name="add_medicine"),
    path('save_medicine/', views.save_medicine, name="save_medicine"),
    path('display_medicine/', views.display_medicine, name="display_medicine"),
    path('edit_medicine/<int:m_id>/', views.edit_medicine, name="edit_medicine"),
    path('delete_medicine/<int:m_id>/', views.delete_medicine, name="delete_medicine"),
    path('update_medicine/<int:m_id>/', views.update_medicine, name="update_medicine"),


]
