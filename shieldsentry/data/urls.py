from django.contrib import admin
from django.urls import path
from .views import signup
from data import views

urlpatterns = [
    path("", views.signup, name="signup"),
    #path("login", login, name="login")
    ]