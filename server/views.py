from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import User
from .models import Dasan
from .models import Record
#import RPi.GPIO as GPIO
import time
import logging
from datetime import datetime
servo_pin=18

def main(request):
    if request.method=='POST':
        '''GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        pwm=GPIO.PWM(servo_pin, 50)

        pwm.start(3.0)
        pwm.ChangeDutyCycle(12.5)
        time.sleep(1.0)
        pwm.stop()
        GPIO.cleanup()'''
        return render(request, 'server/main.html');
        #return render(request, 'server/index.html', {'POST':request.POST['one']});
        
    if request.method=='GET':
        '''GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        pwm=GPIO.PWM(servo_pin, 50)
        
        pwm.start(3.0)
        pwm.ChangeDutyCycle(3.0)
        time.sleep(1.0)
        pwm.stop()
        GPIO.cleanup()'''
        return render(request, 'server/main.html', {'GET':"test"});

def borrow(request):
    if Record.objects.filter(user_id=request.session['user'],borrow_status=1).exists():
        return redirect(select)
    return render(request, 'server/borrow.html', forcast(request));
def cur_status(request):
    bannaptmp=Record.objects.filter(user_id=request.session['user'],borrow_status=0)
    context=forcast(request)
    context['bannaptmp']=bannaptmp
    try:
        borrowtmp=Record.objects.get(user_id=request.session['user'],borrow_status=1)
        context['borrowtmp']=borrowtmp
        return render(request, 'server/cur_status.html', context);
    except:
        context['borrowtmp']=0
        return render(request, 'server/cur_status.html', context);

def dasan(request):
    dasanu=Dasan.objects.all()
    return render(request, 'server/dasan.html', {'dasan':dasanu});

def yangjae(request):
    return render(request, 'server/yangjae.html');


def user_info(request):
    userinf=User.objects.get(user_id=request.session['user'])
    if request.method=='POST':
        userinf.nickname=request.POST['nickname']
        userinf.hakbu=request.POST['hakbu']
        userinf.hakgwa=request.POST['hakgwa']
        userinf.save()
        return redirect(user_info)
    return render(request, 'server/user_info.html', {'user':userinf});
    
def profile(request):
    return render(request, 'server/profile.html');

def money(request):
    return render(request, 'server/money.html');

def app_info(request):
    return render(request, 'server/app_info.html');

def login(request):    
    if(request.method=="POST"):
        users=User.objects.all()
        IDtmp=request.POST['user_id']
        try:
            user=User.objects.get(user_id=IDtmp)
            if(user.password==request.POST['password']):
                response=render(request,'server/main.html')
                request.session['user'] = user.user_id
                return redirect(select)
            return redirect(login)
        except:
            return redirect(login)
    return render(request, 'server/login.html');

def signup(request):
    if(request.method=="POST"):
        id=User.objects.filter(user_id=request.POST['user_id']).count()
        print(id)
        if(id!=0):
            return redirect(signup);
        User.objects.create(user_id=request.POST['user_id'], password=request.POST['password'])
        return redirect(login)
    return render(request, 'server/signup.html');
    
    
def dasan_result(request):
    num=request.GET.get('dasan_btn')
    print("1")
    print(datetime.now().date())
    Record.objects.create(user_id=request.session['user'], borrow_location="다산관", borrow_date=datetime.now().date(), borrow_status=1)
    dasantmp=Dasan.objects.get(dasan_no=num)
    dasantmp.used=0
    dasantmp.save()
    print(dasantmp.used)
    open_door()
    return redirect(dasan)


def test(request):
    return render(request, 'server/test.html');


def select(request):
    context=forcast(request)
    print(Record.objects.filter(user_id=request.session['user'],borrow_status=1).count())
    if Record.objects.filter(user_id=request.session['user'],borrow_status=1).count()>=1:
        context['status']='1'
    else:
        context['status']='0'
    return render(request, 'server/select.html',context);

def bannap(request):
    return render(request, 'server/bannap.html',forcast(request));

def bannap_dasan(request):
    dasanu=Dasan.objects.all()
    return render(request, 'server/bannap_dasan.html', {'dasan':dasanu});

def bannap_dasan_result(request):
    num=request.GET.get('dasan_btn')
    dasantmp=Dasan.objects.get(dasan_no=num) 
    #'select * from Dasan where dasan_no=num'
    dasantmp.used=1
    dasantmp.save()
    recordtmp=Record.objects.get(user_id=request.session['user'],borrow_status=1)
    recordtmp.borrow_status=0
    recordtmp.bannap_location="다산관"
    recordtmp.bannap_date=datetime.now().date()
    recordtmp.save()
    open_door()
    return redirect(bannap_dasan)

def open_door():
    """ GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm=GPIO.PWM(servo_pin, 50)

    pwm.start(3.0)
    pwm.ChangeDutyCycle(11.0)
    time.sleep(5.0)
    pwm.ChangeDutyCycle(6.5)
    time.sleep(1.0)
    pwm.stop()
    GPIO.cleanup() """
    
# test
    

    
import requests

def forcast(request):
    #daily data through API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d24d677a63969b3ec1671db99f1b0218'

    # city variable change it to change the data. For ex. New York
    city = 'Seoul'
    city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types

    #daily weather data
    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'temperature_max': city_weather['main']['temp_max'] ,
        'temperature_min':  city_weather['main']['temp_min']  ,
        'feelslike_weather': city_weather['main']['feels_like']

    }

    #forcasted weather data API
    v = 'http://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid=d24d677a63969b3ec1671db99f1b0218'
    a = v.format(city)
    #accessing the API json data
    full = requests.get(a).json()

    # today's date taking as int
    day = datetime.today()
    today_date = int(day.strftime('%d'))


    forcast_data_list = {} # dictionary to store json data

    #looping to get value and put it in the dictionary
    for c in range(0, full['cnt']):
        date_var1 = full['list'][c]['dt_txt']
        date_time_obj1 = datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
        # print the json data and analyze the data coming to understand the structure. I couldn't find the better way
        # to process date
        if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
            # print(date_time_obj1.strftime('%d %a'))
            if int(date_time_obj1.strftime('%d')) == today_date+1:
                today_date += 1
            forcast_data_list[today_date] = {}
            forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
            forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
            forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
            forcast_data_list[today_date]['FeelsLike'] = full['list'][c]['main']['feels_like']

            forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
            forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
            forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']

            forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
            forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']

            today_date += 1
        else:
            pass
    #returning the context with all the data to the index.html
    context = {
        'weather':weather, 'forcast_data_list':forcast_data_list
    }

    return context
