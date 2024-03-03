from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login,name="login"),
    path('',views.home,name="home"),
    path('create_instance/', views.create_instance,name="create_instance"),
    path('generate_qr/<int:instance_id>',views.generate_qr,name='generate_qr'),
    path('messaging/<int:instance_id>',views.messaging,name='messaging'),
    
]
