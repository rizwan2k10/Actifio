from django.contrib.auth.models import User

from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = ('id', 'username', 'email')




# class Inventoryserializer(serializers.ModelSerializer):
#     class Meta:
#         model=Inventory
#         data = serializers.Field()
#         fields=('data')

class SimpleDataSerializer(serializers.ModelSerializer):
    data = serializers.ListField

    class Meta:
        model = SimpleData
        fields = ["data"]


class get_commandsserializer(serializers.ModelSerializer):

    class Meta:
        model= user_execution_session_log
        fields=['username','command','starttime','endtime','session_exe_id']


class UserSessionLog(serializers.ModelSerializer):

    class Meta:
        model = user_execution_session_log
        fields = ['username', 'command', 'starttime', 'endtime', 'session_exe_id']

# class command_serializr(serializers.ModelSerializer):
#     command = serializers.CharField
#
#     class Meta:
#         model = get_commands
#         fields = []
