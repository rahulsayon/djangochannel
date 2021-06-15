import json
import channels
from django.shortcuts import render
from django.http import HttpResponse
from channels.consumer import get_channel_layer
from asgiref.sync import async_to_sync
import time

from home.thread import *

# Create your views here.

@async_to_sync
async def homeview(request):
    
    for i in range(1):
        channel_layer = get_channel_layer()
        data = { 'count' : i}
        await(channel_layer.group_send)(
            'new_consumer_group', {
            'type' : 'send_notification',
             'value' : json.dumps(data)
            }
        )
        time.sleep(1)
        print("yes")
    return render(request,"home.html")

from django.http import JsonResponse

def generate_student_data(request):
    total = request.GET.get('total')
    CreateStudentThread(int(total)).start()
    return JsonResponse({ 'status' : 200 })