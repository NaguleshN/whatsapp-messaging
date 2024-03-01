from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login,name="login"),
    path('create_instance/', views.create_instance,name="create_instance"),
    path('',views.home,name="home"),
    path('generate_qr/<int:instance_id>',views.generate_qr,name='generate_qr'),
]
