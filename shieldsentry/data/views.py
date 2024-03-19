from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import *
from datetime import datetime
from email.message import EmailMessage
import smtplib
import random
import string


def set_cookie(response, key, value, days_expire=30):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires
    )

def register(request):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                pass
            elif request.COOKIES['log'] == 'a':
                pass
            else:
                pass
        else:
            pass
    elif request.method == "POST":
        name=request.POST['name']
        password=request.POST['password']
        mail=request.POST['mail']
        if name=="" or name==" " or len(password)<8 or '@' in mail:
            pass
        else:
            obj=appuser.objects.create(uname=name,pas=password,email=mail)
            obj.save()
            # response=HttpResponseRedirect(reverse('home'))
            # set_cookie(response,'username', usname)
            # set_cookie(response,'passwd', passwd)
            # set_cookie(response,'log','s')
            # return response

def login(request):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                pass
            elif request.COOKIES['log'] == 'a':
                pass
            else:
                pass
        else:
            pass
    elif request.method == "POST":
        name=request.POST['name']
        password=request.POST['password']
        obj=appuser.objects.filter(uname=name, pas=password)
        if obj:
            # response=HttpResponseRedirect(reverse('home'))
            # set_cookie(response,'username', usname)
            # set_cookie(response,'passwd', passwd)
            # set_cookie(response,'log','s')
            # return response
            pass
        else:
            pass

def home(request,uid=None):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.get(uid=uid)
            elif request.COOKIES['log'] == 'a':
                pass
            else:
                pass
        else:
            pass

def admin(request,uid=None):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                pass
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.get(uid=uid)
            else:
                pass
        else:
            pass

def profile(request,uid=None):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.get(uid=uid)
            elif request.COOKIES['log'] == 'a':
                pass
            else:
                pass
        else:
            pass
    elif request.method == "POST":
        userobj=appuser.objects.get(uid=uid)
        existing_keys=appuser.objects.values_list('api').values()
        key_length=16
        while True:
            api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=key_length))
            if api_key not in existing_keys:
                userobj.api=api_key
                break

def changePassword(request,uid=None):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.get(uid=uid)
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.get(uid=uid)
            else:
                pass
        else:
            pass
    elif request.method == "POST":
        userobj=appuser.objects.get(uid=uid)
        oldpw=request.POST["oldpassword"]
        newpw=request.POST["newpassword"]
        if(userobj.pas==oldpw and len(newpw)>=8):
            userobj.pas=newpw
            userobj.save()
        else:
            pass

def logout(request):
    # response=HttpResponseRedirect(reverse('login'))
    # response.delete_cookie("username")
    # response.delete_cookie("passwd")
    # response.delete_cookie("log")
    # return response
    pass

def checkText(request,api_key=None,uid=None):
    if request.method=="GET":
        if api_key!=None:
            userobj=appuser.objects.get(api=api_key)
        elif uid!=None:
            userobj=appuser.objects.get(uid=uid)
        else:
            pass
        