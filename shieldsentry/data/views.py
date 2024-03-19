from django.shortcuts import render

def signup(request):
        return render(request,"signup.html")


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
            return render(request,"user_dashboard.html")
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

def checkText(request,api_key=None,uid=None,new_message=None):
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
        data = pd.read_csv('SPAM-ALERTSYSTEM-main\spam.csv', encoding='latin-1')

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
            print("spam")
        else:
            print("not spam")
            
def picspam(request,api_key=None,uid=None):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract\tesseract.exe'
    image_path = 'image.jpg'
    image = cv2.imread(image_path)
    text = pytesseract.image_to_string(image)
    print("Text extracted from the selected portion of the image:")
    print(text)
    
