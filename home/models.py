import channels
from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    notification = models.TextField(max_length=200)
    is_seen = models.BooleanField(default=False)
    
    def save(self,*args,**kwargs):
        channels_layer = get_channel_layer()
        notification_obj = Notification.objects.filter(is_seen=False).count()
        data = {"count" : notification_obj}
        
        async_to_sync(channels_layer.group_send)(
            'test_consumer_group',{
                'type' : 'send_notification',
                'value' : json.dumps(data)
            }
        )
        super(Notification,self).save(*args,**kwargs)
        
class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    age = models.IntegerField()