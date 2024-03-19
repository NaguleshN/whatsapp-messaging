from django.shortcuts import render
from messaging_app.urls import path
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import uuid
from messaging_app.models import Instance,Message,Log,Whatsapp_config
import requests
import ssl
import time
from django.contrib import messages
from openpyxl import load_workbook
from whatsapp.settings import BASE_URL
from django.http import HttpResponse, FileResponse
from messaging_app.tasks import send_message,delete_instance_api
import os
from django.conf import settings
from django.utils import timezone
from celery import Celery
from datetime import datetime
from django.http import HttpResponse
import mimetypes
from whatsapp.settings import SAMPLE_EXCEL_PATH



def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        if username is None:
        
            error_message = "Username is not provided."
            messages.error(error_message)
            print(ve)
            return redirect("login")
        
        password=request.POST.get('password')
        if password is None:
                error_message = "password is not provided."
                messages.error(error_message)
                print(ve)
                return redirect("login")
            
        print(username,"-->",password)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            print(" --Accepted-- ")
            auth.login(request,user)
            messages.success(request, 'You are successfully logged in.')
            return redirect('home')
        else:
            error_message = "Invalid username and password."
            messages.error(error_message)
            print(ve)
            return redirect("login")
        
    return render(request,"login.html")


@login_required(login_url='login')
def home(request):

    if request.method=="POST":
 
        instance_name = request.POST.get('instance_name')
        if instance_name is None:
            messages.error("Instance name is not provided.")
            print(ve)
            return redirect("home")
        
        instance_key = uuid.uuid4().hex
        instance_token = "instancetoken"
        user_id=request.user.id
        print(request.user.id)
        user=User.objects.get(id=user_id)
        
        filtered_objects = Instance.objects.filter(user_id=user)
        count = filtered_objects.count()

        if count >= 3:
            messages.error(request, 'You can only create 3 Chatspheres .')
            print("Number of filtered objects:", count)
            print("Count exceeded")
            return redirect('home') 
        print(instance_key,"  ",instance_token)
        try:
            url=BASE_URL+f"/instance/init?key={instance_key}&token={instance_token}"
            response = requests.get(url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            message.error(request,"An error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            message.error(request,"HTTP error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
            message.error(request,"Connection error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
            message.error(request,"Request timed out while processing your request.")
            return redirect('home')

        except requests.exceptions.TooManyRedirects as e:
            print(f"Too many redirects: {e}")
            message.error(request,"Too many redirects occured while processing your request.")
            return redirect('home')

        except requests.exceptions.SSLError as e:
            print(f"SSL certificate error occurred: {e}")
            message.error(request,"SSL certificate error occurred while processing your request.")
            return redirect('home')
                
        except Exception as e:
            print(e)
            print("An error occured on check info url response.")
            message.error(request,"An error occured on check info url response.")
            return redirect('home') 
            
        
        print(response.text)
        print(response)
        
        if response.status_code==200:
            print("instance created")

        try:
            Instance.objects.create(user_id=request.user,instance_name=instance_name,instance_key=instance_key,instance_token=instance_token )
            messages.success(request, 'Chatsphere created successfully. Please scan the QR code to start messaging.')
            print(" created instance ")
            return redirect('home')
        
        except IntegrityError as e:
            print(e)
            messages.error(request, 'Failed to create Chatsphere. Please try again.')
            return redirect('home')
        
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to create Chatsphere. Please try again.')
            return redirect('home')
        return redirect('home')
    user_instances=Instance.objects.filter(user_id=request.user)
    print(user_instances)

    return render(request,"home.html",{"user_instances":user_instances})


@login_required(login_url='login')
def logout(request):
    try:
        auth.logout(request)
    except Exception as e:
        messages.error(request, 'An error occurred while authentication.')
        print(e)
        return redirect("home")
    return redirect("login")


@login_required(login_url='login')
def messaging(request,instance_id):
    success_message = request.GET.get('success')
    if success_message:
            messages.success(request ,"You successfully scanned QR .") 
            instance=Instance.objects.get(id=instance_id)
            instance.qrscanned=True
            instance.save()
    try:
        instance=Instance.objects.get(id=instance_id)
    except Exception as e:
        print(e)
    
    try:
        check_url=BASE_URL+f"/instance/info?key={instance.instance_key}"
        check_response=requests.get(check_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        check_json=check_response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        check_json = {}
        message.error(request,"An error occurred while processing your request.")
        return redirect('home')

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        message.error(request,"HTTP error occurred while processing your request.")
        return redirect('home')

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        message.error(request,"Connection error occurred while processing your request.")
        return redirect('home')

    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        message.error(request,"Request timed out while processing your request.")
        return redirect('home')

    except requests.exceptions.TooManyRedirects as e:
        print(f"Too many redirects: {e}")
        message.error(request,"Too many redirects occured while processing your request.")
        return redirect('home')

    except requests.exceptions.SSLError as e:
        print(f"SSL certificate error occurred: {e}")
        message.error(request,"SSL certificate error occurred while processing your request.")
        return redirect('home')
            
    except Exception as e:
        print(e)
        print("An error occured on check info url response.")
        message.error(request,"An error occured on check info url response.")
        return redirect('home') 
        
    print(check_json)
    instance_data = check_json.get('instance_data', {})  
    user_data = instance_data.get('user', {}) 
    string=user_data['id']
    print(user_data)
    
    instance.phone_number=string[0:12]
    instance.qrscanned=True
    instance.save()
    print(instance.phone_number)
    
    
    try:
        instance=Instance.objects.get(id=instance_id)
    except Instance.DoesNotExist as e:
        print(e)
        messages.error(request,"Instance not found.")
        return redirect("home")
    except Exception as e:
        print(e)
        messages.error(request,"An error occurred while processing your request.")
        return redirect("home")
    
    if request.method=="POST":
        send_message_url=BASE_URL+f"/message/text?key={instance.instance_key}"
        message_context = request.FILES.get('message')
        print(message_context)
        
        try:
            whatsapp_config=Whatsapp_config.objects.get(key=1)
        except Exception as e:
            whatsapp_config=Whatsapp_config.objects.create(key=1,excel_count=0)
            
        whatsapp_config.excel_count=whatsapp_config.excel_count+1
        count=whatsapp_config.excel_count
        print(count)
        whatsapp_config.save()
        
        print(whatsapp_config.excel_count)
        
        excel_name="Excel_"+str(count)+".xlsx"
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', excel_name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in message_context.chunks():
                destination.write(chunk)
        print(message_context.name)
        try: 
            new_log=Log.objects.create(user=request.user,instance=instance,excel_sheet=file_path,excel_name=excel_name,started_at=datetime.now(),successfull=False)

        except Exception as e:
            print(e)
            messages.error(request,"Failed to create log.")
            return redirect("home")

        try:
            send_message.delay(file_path, instance_id,new_log.id)
            messages.success(request,"Request sent successfully.")
        except Exception as e:
            print(e)
            messages.error(request,"Failed to send request to task.")
            return redirect("home")
        
        return redirect('home')

        

    return render(request,"messaging.html",{"instance":instance})


@login_required(login_url='login')
def delete_all_messages(request):
    try:
        instances =Instance.objects.all()
        for instance in instances:
            try:
                delete_instance_api.delay(instance.instance_key)
                instance.delete()
            except Exception as e:
                print("Exception on delete reponse to api")
                messages.error(request,"Error occurred while sending delete request to tasks.")
                print(e)
                return redirect("home")
                
    except Exception as e:
        print("Exception on delete instance")
        messages.error(request,"Error occurred while processing your request.")
        print(e)
        return redirect("home")
    return redirect('home')

@login_required(login_url='login')
def Log_view(request):
    try:
        instances=Instance.objects.filter(user_id=request.user)
        logs=[]
        for instance in instances:
            logs+=Log.objects.filter(instance=instance)
    except Exception as e:
        print("Log is not found ")
        messages.error(request,"Log is not found .")
        print(e)
        return redirect('home')
    return render(request,"logs.html",{"logs":logs})


@login_required(login_url='login')
def delete_instance(request,instance_id):
    
    try:
        instance =Instance.objects.get(id=instance_id)
        print(instance)
    
        delete_url= BASE_URL+f"/instance/delete?key={instance.instance_key}"
        print(delete_url)
        
        instance.delete()
        try:
            delete_response = requests.delete(delete_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
            time.sleep(2)
        except Exception as e:
            print("Exception on delete reponse to api")
            messages.error(request,"Error occurred while getting delete reponse from api.")
            print(e)
            return redirect('home')
            
    except Instance.DoesNotExist as e:
        print(e)
        messages.error(request,"Instance not found.")
        return redirect('home')
    except Exception as e:
        print("Exception on delete instance")
        print(e)
        return redirect('home')
    return redirect('home')


@login_required(login_url='login')
def sample_excel_file(request):
    
    try:
        excel_path=SAMPLE_EXCEL_PATH
        if os.path.exists(excel_path):
            with open(excel_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type=mimetypes.guess_type(excel_path)[0])
                response['Content-Disposition'] = 'attachment; filename="Sample_excel.xlsx"'
                return response
        else:
            return HttpResponse("File not found")
    except Exception as e:
        print("Error occured on sample excel file")
        messages.error(request,"Error occurred while getting the sample excel file.")
        print(e)


@login_required(login_url='login')
def generate_qr(request,instance_id):
    
    try:
    
        instance=Instance.objects.get(id=instance_id)
        try:
            init_url=BASE_URL+f"/instance/init?key={instance.instance_key}&token={instance.instance_token}"
            print(init_url)
            init_response = requests.get(init_url,verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None,  headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
        
        except requests.exceptions.RequestException as e:
            print("An error occurred while processing your request.")
            message.error(request,"An error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            message.error(request,"HTTP error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
            message.error(request,"Connection error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
            message.error(request,"Request timed out while processing your request.")
            return redirect('home')

        except requests.exceptions.TooManyRedirects as e:
            print(f"Too many redirects: {e}")
            message.error(request,"Too many redirects occured while processing your request.")
            return redirect('home')

        except requests.exceptions.SSLError as e:
            print(f"SSL certificate error occurred: {e}")
            message.error(request,"SSL certificate error occurred while processing your request.")
            return redirect('home')
                
        except Exception as e:
            print(e)
            print("An error occured on check info url response.")
            message.error(request,"An error occured on check info url response.")
            return redirect('home') 
            
        time.sleep(2)
        try:
            qr_url2=BASE_URL+f"/instance/qrbase64?key={instance.instance_key}"
            qr_response=requests.get(qr_url2, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
            print(qr_response)
            print(qr_response.text)
            qr_response1=qr_response.json()
            qrcode=qr_response1.get('qrcode',{})
            print(qrcode)
        except requests.exceptions.RequestException as e:
            print("An error occurred while processing your request.")
            message.error(request,"An error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            message.error(request,"HTTP error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
            message.error(request,"Connection error occurred while processing your request.")
            return redirect('home')

        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
            message.error(request,"Request timed out while processing your request.")
            return redirect('home')

        except requests.exceptions.TooManyRedirects as e:
            print(f"Too many redirects: {e}")
            message.error(request,"Too many redirects occured while processing your request.")
            return redirect('home')

        except requests.exceptions.SSLError as e:
            print(f"SSL certificate error occurred: {e}")
            message.error(request,"SSL certificate error occurred while processing your request.")
            return redirect('home')
                
        except Exception as e:
            print(e)
            print("An error occured on check info url response.")
            message.error(request,"An error occured on check info url response.")
            return redirect('home') 
        
        
        
        time.sleep(2)
        
        try:
            check_url=BASE_URL+f"/instance/info?key={instance.instance_key}"
            check_response=requests.get(check_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
            check_json=check_response.json()
        
            print(check_json)
            instance_data = check_json.get('instance_data', {})  
            user_data = instance_data.get('user', {}) 

            if not user_data:
                print("User data is empty.")
                return render(request,"qr2.html",{"instance_id":instance_id,"instance_key":instance.instance_key})
            else:
                print("User data is not empty.")

            messages.success(request, 'Start messaging ... ')
            print(instance.qrscanned)
            instance.qrscanned=True
            instance.save()
            print("updated successfully")
            return redirect('home')
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")

        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")

        except requests.exceptions.TooManyRedirects as e:
            print(f"Too many redirects: {e}")

        except requests.exceptions.SSLError as e:
            print(f"SSL certificate error occurred: {e}")

        except Exception as e:
            print(e)
            print("An error occured on check info url response.")

    except Exception as e:
        print("An error occurred while processing the request.")
        print(e)
        return redirect('home')

