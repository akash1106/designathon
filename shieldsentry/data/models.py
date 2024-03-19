from django.db import models

# Create your models here.
class user(models.Model):
    uid=models.AutoField(primary_key=True,unique=True)
    uname=models.CharField(max_length=100)
    pas=models.CharField(max_length=25)
    email=models.EmailField()
    api=models.CharField(max_length=36,default='')  #api key for the app
    usage=models.IntegerField(default=0)     #number of times used
