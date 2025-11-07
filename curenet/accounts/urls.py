from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/create/patient/', views.create_patient_profile, name='create_patient_profile'),
    path('profile/create/doctor/', views.create_doctor_profile, name='create_doctor_profile'),
    path('dashboard/', views.profile_redirect, name='profile_redirect'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
]

