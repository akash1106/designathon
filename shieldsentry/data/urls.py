<<<<<<< HEAD
from django.contrib import admin
from django.urls import path
from .views import signup
from data import views

urlpatterns = [
    path("", views.signup, name="signup"),
    #path("login", login, name="login")
    ]
=======
from unicodedata import name
from django.urls import path
from . import views
urlpatterns=[
    path("",views.login,name="login"),
]
>>>>>>> 9f4f27808ad8522efbca7d8a50fc608262f973fa
