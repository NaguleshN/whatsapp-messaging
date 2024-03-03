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
from django.contrib import messages
from openpyxl import load_workbook


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

    
@login_required(login_url='login')
def generate_qr(request,instance_id):
    instance=Instance.objects.get(id=instance_id)
    try:
        
        init_url=f"http://localhost:3333/instance/init?key={instance.instance_key}&token={instance.instance_token}"
        print(init_url)
        init_response = requests.get(init_url,verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        
        time.sleep(2)
        
        qr_url=f"http://localhost:3333/instance/qr?key={instance.instance_key}"
        qr_response=requests.get(qr_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        
        print(qr_response)
        print(qr_response.text)
        
        time.sleep(2)
        
        check_url=f"http://localhost:3333/instance/info?key={instance.instance_key}"
        check_response=requests.get(check_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        check_json=check_response.json()
        
        print(check_json)
        print(check_response.text)
        instance_data = check_json.get('instance_data', {})  
        user_data = instance_data.get('user', {}) 

        if not user_data:
            print("User data is empty.")
            return render(request,"qr.html",{"qr":qr_response.text,"instance_id":instance_id})
        else:
            print("User data is not empty.")
            
            messages.success(request, 'Start messaging ... ')
            print(instance.qrscanned)
            instance.qrscanned=True
            instance.save()
            print("updated successfully")
            return redirect('home')
    
        return render(request,"qr.html",{"qr":qr_response.text,"instance_id":instance_id})
    
    except Exception as e:
        print(e)
        print(instance)
    return redirect('home')

@login_required(login_url='login')
def messaging(request,instance_id):
    instance=Instance.objects.get(id=instance_id)
    if request.method=="POST":
        
        send_message_url=f"http://localhost:3333/message/text?key={instance.instance_key}"
        message_context = request.FILES.get('message')
        print(type(message_context))
        print(message_context)
        if message_context:
            wb = load_workbook(message_context)
            sheet = wb.active
            # for row in sheet.iter_rows(values_only=True):
            #     for cell_value in row:
            #         print(cell_value)
                    
            data = []
            init_url=f"http://localhost:3333/instance/init?key={instance.instance_key}&token={instance.instance_token}"
            print(init_url)
            init_response = requests.get(init_url,verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        
            time.sleep(2)
            for row in sheet.iter_rows(values_only=True):
                if len(row) >= 2: 
                    data.append((row[0], row[1]))
            print(data) 
            for i in data:
                print(i[0],i[1])
                body_data = {
                    "id": i[0],
                    "message": i[1]
                }
                try:
                    response=requests.post(send_message_url, data=body_data , verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, auth=None, hooks=None, json=None, params=None)
                    time.sleep(2)
                    print(send_message_url)
                    print(response.text)
                    print(response)
                    if response.status_code >= 200 and response.status_code < 300:
                        print("Request sent successfully.")
                        messages.success(request, f"Message sent successfully for {i[0]}")
                    else:
                        print(f"Failed to send request. Status code: {response.status_code}")
                        messages.error(request, f"Failed to send message for {i[0]}. Please try again.")       
                except Exception as e:
                    print(e)
        return redirect('home')
    return render(request,"messaging.html",{"instance":instance})