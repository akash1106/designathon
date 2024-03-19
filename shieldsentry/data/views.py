from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import  HttpResponseRedirect
from django.urls import reverse
from datetime import datetime,timedelta
import random
import string
import pandas as pd
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import nltk
import cv2
import pytesseract
from django.shortcuts import render
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .forms import *
from PIL import Image


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.strftime(
        datetime.utcnow() + timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires
    )
    
def register(request):
    print("ukjsd,m")
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.filter(uname=name, pas=password)
                if userobj:
                    return HttpResponseRedirect(reverse('home',args=[userobj.uid]))
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.filter(uname=name, pas=password)
                if userobj:
                    return HttpResponseRedirect(reverse('admindesh',args=[userobj.uid]))
            return render(request,"signup.html")
        else:
            return render(request,"signup.html")
    elif request.method == "POST":
        name=request.POST['name']
        password=request.POST['password1']
        mail=request.POST['mail']
        print(1)
        if name=="" or name==" " or len(password)<8 or not '@' in mail:
            pass
        else:
            print(2)
            obj=appuser.objects.create(uname=name,pas=password,email=mail)
            obj.save()
            print(obj.uid)
            response=HttpResponseRedirect(reverse('home',args=[obj.uid]))
            set_cookie(response,'username', mail)
            set_cookie(response,'passwd', password)
            set_cookie(response,'log','s')
            return response

def login(request):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.filter(email=request.COOKIES['username'], pas=request.COOKIES['passwd'])
                if userobj:
                    return HttpResponseRedirect(reverse('home',args=[userobj[0].uid]))
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.filter(uname=name, pas=password)
                if userobj:
                    return HttpResponseRedirect(reverse('admindesh',args=[userobj.uid]))
            return render(request,"login.html")
        else:
            return render(request,"login.html")
    elif request.method == "POST":
        name=request.POST['name']
        password=request.POST['password']
        obj=appuser.objects.filter(email=name, pas=password)
        print(obj)
        if obj:
            response=HttpResponseRedirect(reverse('home',args=[obj[0].uid]))
            set_cookie(response,'username', name)
            set_cookie(response,'passwd', password)
            set_cookie(response,'log','s')
            return response
        else:
            return 

def home(request,uid=None):
    if request.method == "GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.filter(uid=uid)
                return  render(request,"user_dashboard.html",{
                    "user":userobj[0],
                    })
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.filter(uname=request.COOKIES['username'], pas=request.COOKIES['passwd'])
                if userobj:
                    return HttpResponseRedirect(reverse('admindesh/'+str(userobj.uid)))
            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('login'))

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
                userobj=appuser.objects.filter(uid=uid)
                return render(request,"admin_profile.html",{
                    "user":userobj[0],
                })
            elif request.COOKIES['log'] == 'a':
                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('login'))
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
                return  render(request,'changepw.html',{'uesr':userobj})
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.get(uid=uid)
            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('login'))
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
    response=HttpResponseRedirect(reverse('login'))
    response.delete_cookie("username")
    response.delete_cookie("passwd")
    response.delete_cookie("log")
    return response

def checkText(request,api_key=None,uid=None):
    if request.method=="POST":
        if api_key!=None:
            userobj=appuser.objects.get(api=api_key)
            new_message = request.form['message']
        elif uid!=None:
            userobj=appuser.objects.get(uid=uid)
        else:
            pass
        userobj.usage+=1
        userobj.save()
        new_message = request.POST['message']
        res=texttest(new_message)
        if res:
            print("not spam")
            return render(request,"text_detection.html",{
                "user":userobj,
                "data":2,
                "place":new_message,
            })
        else:
            print("spam")
            return render(request,"text_detection.html",{
                "user":userobj,
                "data":1,
                "place":new_message,
            })
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.filter(email=request.COOKIES['username'], pas=request.COOKIES['passwd'])
                print(userobj)
                if userobj:
                    return render(request,"text_detection.html",{
                        "user":userobj[0],
                        "data":0,
                        "place":'',
                    })
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.filter(uid=uid)
                if userobj:
                    return HttpResponseRedirect(reverse('admindesh',args=[userobj[0].uid]))
            return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('login'))
               
def picspam(request,api_key=None,uid=None):
    if request.method=="POST":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract\tesseract.exe'
        
        uploaded_image = request.FILES['image']
        with open('uploaded_image.png', 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)
        
        image = Image.open('uploaded_image.png')
        text = pytesseract.image_to_string(image)
        res=texttest(text)
        userobj=appuser.objects.filter(uid=uid)
        if res:
            return render(request,"img_dtection.html",{
                "user":userobj[0],
                "data":1,
            })
        else:
            return render(request,"img_dtection.html",{
                "user":userobj[0],
                "data":2,
            })
    elif request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.filter(email=request.COOKIES['username'], pas=request.COOKIES['passwd'])
                if userobj:
                    return render(request,'img_dtection.html',{
                        "user":userobj[0],
                        "data":0,
                    })
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.filter(email=request.COOKIES['username'], pas=request.COOKIES['passwd'])
                if userobj:
                    return HttpResponseRedirect(reverse('login'))
            return render(request,"login.html")
        else:
            return render(request,"login.html")
     
def texttest(mess):
        new_message=mess
        data = pd.read_csv('D:\\akash\\designathon\\shieldsentry\\data\\spam.csv', encoding='latin-1')

        stop_words = set(stopwords.words('english'))

        def preprocess_text(text):
            text = re.sub('[^a-zA-Z]', ' ', text)
            text = text.lower()
            text = nltk.word_tokenize(text)
            text = [word for word in text if word not in stop_words]
            text = ' '.join(text)
            return text

        data['v2'] = data['v2'].apply(preprocess_text)

        X_train, X_test, y_train, y_test = train_test_split(data['v2'], data['v1'], test_size=0.2, random_state=42)


        vectorizer = CountVectorizer()
        X_train = vectorizer.fit_transform(X_train)
        X_test = vectorizer.transform(X_test)

        clf = MultinomialNB()
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, pos_label='spam')
        recall = recall_score(y_test, y_pred, pos_label='spam')
        f1 = f1_score(y_test, y_pred, pos_label='spam')

        # print("Accuracy:", accuracy)
        # print("Precision:", precision)
        # print("Recall:", recall)
        # print("F1 score:", f1)
        global a11
        a11 = '' + new_message
        print("YOUR INPUT:", a11)
        new_message = preprocess_text(new_message)
        new_message_vector = vectorizer.transform([new_message])
        prediction = clf.predict(new_message_vector)
        if prediction[0] == 'spam':
            return 0
        else:
            return 1
    
def checkaudio(request,api=None,uid=None):
    if request.method=='POST':
        uploaded_audio = request.FILES['audio']
        with open('uploaded_audio.wav', 'wb') as f:
            for chunk in uploaded_audio.chunks():
                f.write(chunk)
        def transcribe_audio(file_path):
            recognizer = sr.Recognizer()
            with sr.AudioFile(file_path) as audio_file:
                audio_data = recognizer.record(audio_file)
            transcription = recognizer.recognize_google(audio_data)
            return transcription
        dataset = pd.read_csv("D:\\akash\\designathon\\shieldsentry\\data\\static\\file\\transcripe.csv")
        transcription = transcribe_audio("uploaded_audio.wav")
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(dataset["transcription"])
        y = dataset["label"]
        model = LogisticRegression()
        model.fit(X, y)
        X_test = vectorizer.transform([transcription])
        y_pred = model.predict(X_test)
        userobj=appuser.objects.filter(uid=uid)
        if y_pred[0] == 1:
            return render(request,"audio_detection.html",{
                        "user":userobj[0],
                        "data":1,
                    })
        else:
            return render(request,"audio_detection.html",{
                        "user":userobj[0],
                        "data":2,
                    })
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                userobj=appuser.objects.filter(email=request.COOKIES['username'], pas=request.COOKIES['passwd'])
                if userobj:
                    return render(request,"audio_detection.html",{
                        "user":userobj[0],
                        "data":0,
                    })
            elif request.COOKIES['log'] == 'a':
                userobj=appuser.objects.filter(email=request.COOKIES['username'], pas=request.COOKIES['passwd'])
                if userobj:
                    return HttpResponseRedirect(reverse('admindesh',args=[userobj.uid]))
            return render(request,"login.html")
        else:
            return render(request,"login.html")

def checkpan():
    pass

def checkaadhar():
    pass