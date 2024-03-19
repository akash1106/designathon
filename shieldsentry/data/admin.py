from django.contrib import admin
from ast import ClassDef
from msilib.schema import Class
from .models import *


class appuserAdmin(admin.ModelAdmin):
    list_display=("uid","uname","pas","email","api","usage")
    
    
admin.site.register(user,appuserAdmin)
