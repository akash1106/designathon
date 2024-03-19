from django.contrib import admin
from django.urls import path
from . import views
urlpatterns=[
    path("",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("home/<int:uid>",views.home,name='home'),
    path("admindash/<int:uid>",views.admin,name="admindesh"),
    path("profile/<int:uid>",views.profile,name="profile"),
    path("changepass/<int:uid>",views.changePassword,name="changepass"),
    path("logout",views.logout,name="logout"),
    path("checkText/<int:uid>",views.checkText,name="checktext"),
    path("picspam/<int:uid>",views.picspam,name="picspam"),
    path("checkaudio/<int:uid>",views.checkaudio,name="checkaudio"),
]