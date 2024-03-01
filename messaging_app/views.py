from django.shortcuts import render
from messaging_app.urls import path
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import uuid
from messaging_app.models import Instance,Message,Log
import requests
import ssl
import time
# Create your views here.


def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,"-->",password)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            print(" --Accepted-- ")
            auth.login(request,user)
            return redirect('home')
    return render(request,"login.html")

@login_required(login_url='login')
def home(request):
    user_instances=Instance.objects.filter(user_id=request.user)  
    print(user_instances)
    return render(request,"home.html",{"user_instances":user_instances})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return render(request,"login.html")

@login_required(login_url='login')
def create_instance(request):
    if request.method=="POST":
        user_id=request.user.id
        instance_key = request.POST['instance_name']
        instance_token = request.POST.get('instance_key')
        print(instance_key,"  ",instance_token)
        try:
            url=f"http://localhost:3333/instance/init?key={instance_key}&token={instance_token}"
            response = requests.get(url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        except Exception as e:
            print(e)
            return render(request,"create_instance.html")
        print(response.text)
        print(response)
        if response.status_code==200:
            print("instance created")
        #     data=response.json()
        Instance.objects.create(user_id=request.user,instance_key=instance_key,instance_token=instance_token )
        print(" created instance ")
        return redirect('home')
    unique_key = uuid.uuid4().hex
  
    return render(request,"create_instance.html",{"unique_key":unique_key})

def init_instance(instance_key,instance_token):
    try:
        url=f"http://localhost:3333/instance/init?key={instance_key}&token={instance_token}"
        response = requests.get(url)
        print(response.text)
        print(response)
        if response.status_code==200:
            print("instance created")
        print("created instance")
    except Exception as e:
        print(e)


def generate_qr(request,instance_id):
    instance=Instance.objects.get(id=instance_id)
    try:
        # init_instance(instance.instance_key,instance.instance_token)
        print(instance.instance_key,instance.instance_token)
        
        url1=f"http://localhost:3333/instance/qr?key={instance.instance_key}"
        response1=requests.get(url1)
        
        print(response1)
        print(response1.text)
        # time.sleep(20)
        
        # check_url=f"http://localhost:3333/instance/info?key={instance.instance_key}"
        # response1=requests.get(check_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        # a=response1.json()
        # print(a)
        # print(response1.text)
        # instance_data = a.get('instance_data', {})  

        # user_data = instance_data.get('user', {}) 

        # if not user_data:
        #     print("User data is empty.")
        #     return render(request,"qr.html",{"qr":response.text,"instance_id":instance_id})
        # else:
        #     print("User data is not empty.")
        #     return redirect('home')
    
        return render(request,"qr.html",{"qr":response1.text,"instance_id":instance_id})
    
    except Exception as e:
        print(e)
    print(instance)
    return redirect('home')
