from django.contrib import admin
from django.urls import path
from . import views
import messaging_app.views as messaging_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.home,name="home"),
    path('login/', views.login,name="login"),
    path('logout/', LogoutView.as_view() ,name="logout"),
    path('log/', views.Log_view,name="log"),
    path('create_instance/', views.create_instance,name="create_instance"),
    path('delete_all_instance/', views.delete_all_messages,name="delete_all_messages"),
    path('delete_instance/<int:instance_id>', views.delete_instance,name="delete_instance"),
    path('generate_qr/<int:instance_id>',views.generate_qr,name='generate_qr'),
    path('messaging/<int:instance_id>',views.messaging,name='messaging'),

]
