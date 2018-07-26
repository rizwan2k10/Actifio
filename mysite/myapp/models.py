from django.db import models
from django.contrib.auth.models import User
import datetime

class SimpleData(models.Model):
    data = []

    def __init__(self):
        self.data = []

    def add(self, data):
        self.data.append(data)

# class user_execution_session_log(models.Model):
#

class user_execution_session_log(models.Model):
    #id=models.CharField(max_length=30,primary_key=True,unique=True)
    # id=models.CharField(auto_now_add=True)
    username = models.CharField(max_length=30)
    command = models.CharField(max_length=500)
    starttime= models.DateTimeField()
    endtime = models.DateTimeField()
    session_exe_id = models.CharField(max_length=100)
   # website = models.URLField()
   #  def __str__(self):
   #      return self.username,self.session_exe_id,self.command
   #
   #  class Meta:
   #      ordering = ['starttime']
   #  def __init__(self, id, username, command, starttime, endtime, session_exe_id):
   #      self.username = username
   #      self.command = command
   #      self.starttime = starttime
   #      self.endtime = endtime
   #      self.session_exe_id = session_exe_id

    # def Meta(self):
    #     verbose_name = ('user_session_exe_log')
    #     abstract = True
    #
    # def update(self, username, command, starttime, endtime, session_exe_id):
    #     # self.
    #     pass
    #
    # def getData(self, username):
    #
# Create your models here.
