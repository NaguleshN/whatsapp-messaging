from celery import shared_task
from openpyxl import load_workbook
import os
from django.http import HttpResponse, FileResponse
from .models import Instance
import logging
import requests
import time
from whatsapp.settings import BASE_URL
from django.contrib import messages
# from messaging_app.models import Instance,Message,Log

#  python -m celery -A whatsapp  worker -l info -P eventlet

logging.basicConfig(filename='celery.log', level=logging.INFO)

@shared_task()
def send_message(excel_path,instance_id):
    logging.info(instance_id)
    instance=Instance.objects.get(id=instance_id)
    # restore_url="http://localhost:3333/instance/restore"
    # restore_response=requests.get(restore_url, verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, data=None, auth=None, hooks=None, json=None, params=None)
    
    send_message_url= BASE_URL+f"/message/text?key={instance.instance_key}"
    if excel_path is not None:
            wb = load_workbook(excel_path)
            sheet = wb.active
            data = []
            for row in sheet.iter_rows(values_only=True):
                if len(row) >= 2: 
                    data.append((row[0], row[1]))
            logging.info(f"Data to be sent: {data}")
            
            for i in data:
                logging.info(f"Sending message for ID: {i[0]}, Message: {i[1]}")
                body_data = {
                    "id": i[0],
                    "message": i[1]
                }
                try:
                    response=requests.post(send_message_url, data=body_data , verify=True, timeout=None, allow_redirects=True, stream=False, proxies=None, headers=None, cookies=None, files=None, auth=None, hooks=None, json=None, params=None)
                    time.sleep(3)
                    logging.info(f"Request URL: {send_message_url}")
                    logging.info(f"Response text: {response.text}")
                    logging.info(f"Response status code: {response.status_code}")
                    
                except Exception as e:
                    logging.error(f"Exception occurred: {e}")
            
            if response.status_code >= 200 and response.status_code < 300:
                messages.success("Request sent successfully.")

            else:
                messages.success(f"Failed to send request. Status code: {response.status_code}")
                
def delete_all_messages():
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
    