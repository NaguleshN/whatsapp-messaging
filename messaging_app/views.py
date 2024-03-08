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
from whatsapp.settings import BASE_URL
from django.http import HttpResponse, FileResponse
from messaging_app.tasks import send_message,delete_all_instance
import os
from django.conf import settings
from django.utils import timezone
from celery import Celery
excel_counter=0


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
    success_message = request.GET.get('success')
    if success_message:
        messages.success(request ,"Your success message here.") 
    user_instances=Instance.objects.filter(user_id=request.user)
    print(user_instances)
    return render(request,"home.html",{"user_instances":user_instances})


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return render(request,"login.html")


@login_required(login_url='login')
def create_instance(request):
    user_id=request.user.id
    if request.method=="POST":
        instance_name = request.POST.get('instance_name')
        instance_key = request.POST.get('instance_key')
        instance_token = "Instance token"
        
        user=User.objects.get(id=user_id)
        filtered_objects = Instance.objects.filter(user_id=user)
        count = filtered_objects.count()
        
        if count >= 3:
            messages.error(request, 'You can only create 3 instances.')
            print("Number of filtered objects:", count)
            print("Count exceeded")
            return redirect('home') 
        print(instance_key,"  ",instance_token)
        try:
            url=BASE_URL+f"/instance/init?key={instance_key}&token={instance_token}"
            response = requests.get(url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        except Exception as e:
            print(e)
            return redirect("create_instance")
        print(response.text)
        print(response)
        if response.status_code==200:
            print("instance created")
        #     data=response.json()
        Instance.objects.create(user_id=request.user,instance_name=instance_name,instance_key=instance_key,instance_token=instance_token )
        messages.success(request, 'Instance created successfully. Please scan the QR code to start messaging.')
        print(" created instance ")
        return redirect('home')
    user=User.objects.get(id=user_id)
    filtered_objects = Instance.objects.filter(user_id=user)
    count = filtered_objects.count()
    print(filtered_objects)
    if count >= 3:
        messages.error(request, 'You can only create 3 instances.')
        print("Number of filtered objects:", count)
        print("Count exceeded")
        return redirect('home') 
    unique_key = uuid.uuid4().hex
    return render(request,"create_instance.html",{"unique_key":unique_key})
    # return render(request,"messaging2.html")

    
@login_required(login_url='login')
def generate_qr(request,instance_id):
    instance=Instance.objects.get(id=instance_id)
    try:
        
        # init_url=BASE_URL+f"/instance/init?key={instance.instance_key}&token={instance.instance_token}"
        # print(init_url)
        # init_response = requests.get(init_url,verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        
        # time.sleep(2)
        
        # qr_url2=BASE_URL+f"/instance/qrbase64?key={instance.instance_key}"
        # qr_url=BASE_URL+f"/instance/qr?key={instance.instance_key}"
        # qr_response=requests.get(qr_url2, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        
        # print(qr_response)
        # print(qr_response.text)
        # qr_response1=qr_response.json()
        # qrcode=qr_response1.get('qrcode',{})
        # print(qrcode)
        # time.sleep(2)
        
        check_url=BASE_URL+f"/instance/info?key={instance.instance_key}"
        check_response=requests.get(check_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        check_json=check_response.json()
        
        print(check_json)
        # print(check_response.text)
        instance_data = check_json.get('instance_data', {})  
        user_data = instance_data.get('user', {}) 

        if not user_data:
            print("User data is empty.")
            return render(request,"qr2.html",{"instance_id":instance_id,"instance_key":instance.instance_key})
            # return render(request,"qr2.html",{"qr":qrcode,"instance_id":instance_id})
        else:
            print("User data is not empty.")
            
            messages.success(request, 'Start messaging ... ')
            print(instance.qrscanned)
            instance.qrscanned=True
            instance.save()
            print("updated successfully")
            return redirect('home')
    
        return render(request,"qr2.html",{"qr":qr_response.text,"instance_id":instance_id,"instance_key":instance.instance_key})
    
    except Exception as e:
        print(e)
        print(instance)
    return redirect('home')

@login_required(login_url='login')
def messaging(request,instance_id):
    success_message = request.GET.get('success')
    if success_message:
        messages.success(request ,"You successfully scanned QR .") 
        instance=Instance.objects.get(id=instance_id)
        instance.qrscanned=True
        instance.save()
        
    global excel_counter
    instance=Instance.objects.get(id=instance_id)
    
    if request.method=="POST":
        send_message_url=BASE_URL+f"/message/text?key={instance.instance_key}"
        message_context = request.FILES.get('message')
        print(type(message_context))
        print(message_context)
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', "Excel_"+str(excel_counter)+".xlsx")
        excel_counter+=1
        with open(file_path, 'wb+') as destination:
            for chunk in message_context.chunks():
                destination.write(chunk)
        print(message_context.name)
        # send_message.delay(message_context,instance_id)
        new_log=Log.objects.create(user=request.user,instance=instance,excel_sheet=file_path,started_at=timezone.now(),ended_at=timezone.now(),successfull=False)
        try:
            send_message.apply_async(args=[file_path, instance_id,new_log.id])
            
            messages.success(request,"Request sent successfully.")
        except Exception as e:
            messages.success(request,"Failed to send request.")
        # if message_context:
        #     wb = load_workbook(message_context)
        #     sheet = wb.active
        #     # for row in sheet.iter_rows(values_only=True):
        #     #     for cell_value in row:
        #     #         print(cell_value)
                    
        #     data = []
        #     # init_url=BASE_URL+f"/instance/init?key={instance.instance_key}&token={instance.instance_token}"
        #     # print(init_url)
        #     # init_response = requests.get(init_url,verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        
        #     # time.sleep(2)
        #     for row in sheet.iter_rows(values_only=True):
        #         if len(row) >= 2: 
        #             data.append((row[0], row[1]))
        #     print(data) 
        #     for i in data:
        #         print(i[0],i[1])
        #         body_data = {
        #             "id": i[0],
        #             "message": i[1]
        #         }
        #         try:
        #             response=requests.post(send_message_url, data=body_data , verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, auth=None, hooks=None, json=None, params=None)
        #             time.sleep(2)
        #             print(send_message_url)
        #             print(response.text)
        #             print(response)
        #             if response.status_code >= 200 and response.status_code < 300:
        #                 print("Request sent successfully.")
        #                 messages.success(request, f"Message sent successfully for {i[0]}")
        #             else:
        #                 print(f"Failed to send request. Status code: {response.status_code}")
        #                 messages.error(request, f"Failed to send message for {i[0]}. Please try again.")       
        #         except Exception as e:
        #             print(e)
        return redirect('home')
    return render(request,"messaging.html",{"instance":instance})

def delete_all_messages(request):
    delete_all_instance.apply_async(args=[])
    instances =Instance.objects.all()
    for instance in instances:
        try:
            print(instance)
            delete_url= BASE_URL+f"/instance/delete?key={instance.instance_key}"
            print(delete_url)
            instance.delete()
            delete_response = requests.delete(delete_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
            time.sleep(2)
        except Exception as e:
            print(e)
    # return render('home.html')
    return redirect('home')


def Log_view(request):
    instance=Instance.objects.filter(user_id=request.user)
    logs=[]
    for i in instance:
        logs+=Log.objects.filter(instance=i)
    # logs=Log.objects.filter(instance=instance)
    return render(request,"logs.html",{"logs":logs})


def delete_instance(request,instance_id):
    instance =Instance.objects.get(id=instance_id)
    try:
        print(instance)
        delete_url= BASE_URL+f"/instance/delete?key={instance.instance_key}"
        print(delete_url)
        instance.delete()
        delete_response = requests.delete(delete_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        time.sleep(2)
    except Exception as e:
        print(e)
    return redirect('home')