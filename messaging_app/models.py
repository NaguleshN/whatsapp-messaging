from django.db import models
from django.contrib.auth.models import User


class Instance(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE) 
    instance_key = models.CharField(max_length=25)
    instance_token = models.CharField(max_length=100)
    qrscanned=models.BooleanField(default=False)
    
    def __str__(self):  
        return self.instance_key


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
    Excel_sheet = models.FileField()
    Started_at = models.DateTimeField('time started')
    Ended_at = models.DateTimeField('time ended')
    Successful = models.BooleanField()

    def __str__(self):
        return self.user.username + " --> "+self.instance.instance_name
