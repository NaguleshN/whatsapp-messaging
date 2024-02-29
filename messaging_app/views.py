from django.shortcuts import render
from messaging_app.urls import path
from django.contrib.auth.models import User,auth
# Create your views here.


def login(request):
    if request.method=="POST":
        username=request.POST.get('usename')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return  render(request,'messaging_app/home')
    return render(request,"login.html")