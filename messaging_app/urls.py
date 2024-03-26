from django.contrib import admin
from django.urls import path
from . import views
import messaging_app.views as messaging_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/', views.login,name="login"),
    path('log/', views.Log_view,name="log"),
    path('logout/', auth_views.LogoutView.as_view() ,name="logout"),
    path('delete_all_instance/', views.delete_all_messages,name="delete_all_messages"),
    path('delete_instance/<int:instance_id>', views.delete_instance,name="delete_instance"),
    path('generate_qr/<int:instance_id>',views.generate_qr,name='generate_qr'),
    path('messaging/<int:instance_id>',views.messaging,name='messaging'),
    path('serve_excel/', views.sample_excel_file, name='serve_excel'),

]
