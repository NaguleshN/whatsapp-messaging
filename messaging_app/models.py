from django.db import models
from django.contrib.auth.models import User


class Instance(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE) 
    instance_name = models.CharField(max_length=50)
    instance_key = models.CharField(max_length=25)
    instance_token = models.CharField(max_length=100)
    qrscanned=models.BooleanField(default=False)
    phone_number=models.CharField(max_length=12,null=True)
    instance_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.instance_name


class Message(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=12)
    message_text = models.CharField(max_length=200)
    message_time = models.DateTimeField('time sent')

    def __str__(self):  
        return self.message_text + " ("+self.instance.instance_name+")"


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    excel_sheet = models.CharField(max_length=100)
    excel_name=models.CharField(max_length=20)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    successfull = models.BooleanField()
        
    def __str__(self):
        return self.user.username + " --> "+self.instance.instance_key

class Whatsapp_config(models.Model):
    key=models.IntegerField()
    excel_count = models.PositiveIntegerField()