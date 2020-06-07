from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.utils import datetime_safe
from django.views.decorators.csrf import csrf_exempt
from os import system

from integration.models import Alarm, Settings

import json

# Create your views here.
def index(request):
    return HttpResponse(content='You are a fucking retard')


@csrf_exempt
def alarms_add(request):
    if request.method != 'POST': return HttpResponse(content='Forbidden', reason=403)
    new_alarm_time = request.POST.get('time', '12:00')
    new_alarm_title = request.POST.get('title', 'Default')
    new_alarm_repeat = request.POST.get('repeat', 'MTWTFSS')
    new_alarm_sound = request.POST.get('sound', 'default')

    new_alarm = Alarm(time=new_alarm_time, title=new_alarm_title, repeat=new_alarm_repeat, sound=new_alarm_sound)
    new_alarm.save()
    create_update_file()
    return HttpResponse(content='Hello World!')


@csrf_exempt
def alarms_remove(request):
    if request.method != 'POST': return HttpResponse(content='Forbidden', reason=403)

    alarm_id = request.POST.get('id', '')
    if alarm_id == '': return HttpResponse(content='No ID provided', reason=400)
    
    Alarm.objects.all()[int(alarm_id)].delete()
    create_update_file()
    return HttpResponse(content='Request parsed')


@csrf_exempt
def alarms_list(request):
    # return HttpResponse('<br />\n'.join([str(x) for x in Alarm.objects.all()]))
    output = '[' + ', '.join([x.to_json() for x in Alarm.objects.all()]) + ']'
    return HttpResponse(content=output)


@csrf_exempt
def datetime_set(request):
    # Set up the date and time
    # Setting the time with system() is a big security flaw (RCE) and I should find an alternative soon.
    sync_time = Settings.objects.filter(setting_id__startswith='sync_time')
    print(f'values: {sync_time.values()}')
    print(f'{sync_time.values()[0]["value"]}.')
    if sync_time.values()[0]["value"]:
        print(f'setting: {sync_time}')
        print(f'new date: {request.POST.get("date")}\nnew time: {request.POST.get("time")}')
        system(f'sudo date -s \"{request.POST.get("date")} {request.POST.get("time")}\"')
        return HttpResponse(content='OK', reason=200)
    else:
        return HttpResponse(content='Not ok', reason=403)


def create_update_file():
    with open('Files/.__update__', 'w+') as update_file:
        update_file.write('lol')
