from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .serializers import UserSerializer, SimpleDataSerializer, get_commandsserializer, UserSessionLog
from rest_framework import viewsets
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpRequest
from rest_framework.response import Response
from .library import asyncio_stream, asyncio_generator
from .serializers import *
from .forms import UserRegistrationForm
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from myapp.library import timer
from rest_framework.decorators import api_view
from .models import *
import os
from django.urls import reverse
import uuid
from django.utils import timezone
import datetime
from django.db.models import Q
from rest_framework import serializers


class UserViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

threader = None


def home(request):
    if not request.session.session_key:
        return render(request, 'logindemo.html')
    else:

        return render(request, 'home.html', {'rc': user_execution_session_log.command.__dict__})
        # return HttpResponseRedirect('/actifio/')


def user_login(request):
        global suser
        # suser=request.session['username']
        context = {}
        if request.method == 'POST':

                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:

                    request.session['username'] = username
                    request.session.modified = True
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    context["error"] = "username or password is not correct"
                    return render(request, 'logindemo.html', context)

            # else:
                # return render(request,'home.html')

        else:
            return render(request, 'logindemo.html')


def user_logout(request):
        del request.session['username']
        logout(request)
        # Redirect back to index page.
        return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                # user = authenticate(username = username, password = password)
                # login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.info(request, message="Username or password already exists")
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})


@api_view(['GET'])
def filenames_host(request):
    global root
    smp = SimpleData()
    root_inv = os.path.join(root, 'inv')
    root_host = os.path.join(root_inv, 'host')
    # "C:/Users/pamid/PycharmProjects/djagoproject/robot/inv/host"
    for path, dirs, files in os.walk(root_host):
            for f in files:
                if f.endswith('.py'):
                    smp.add(str(f))

                    # data = {"data": demo}
    # inventory_files_obj = Inventory.objects.all().values(*demo)
    # serializer = Inventoryserializer(inventory_files_obj, many=True)
    # serializer = SimpleDataSerializer(SimpleData(demo))
    # print(type(smp.data))
    # print(','.join(smp.data))
    # data=SimpleData.objects.filter(id=SimpleData.data)

    # return Response({','.join(smp.data)})
    return Response(smp.__dict__)
# return render(request, )


def get_workspace(request):
    global root
    if request.method == 'POST':
        root = request.POST['views']
        # return HttpResponseRedirect(reverse('appliance'))

        return redirect('/')
    else:

        return HttpResponseRedirect(reverse('home'))


@api_view(['GET'])
def filenames_testcases(request):
    global root
    smp_suites = SimpleData()
    root_testcases = os.path.join(root, 'suites')
    # "C:/Users/pamid/PycharmProjects/djagoproject/robot/suites"
    for path, dirs, files in os.walk(root_testcases):
            for f in files:
                if f.endswith('.robot'):
                    smp_suites.add(f)
    return Response(smp_suites.__dict__)


@api_view(['GET'])
def filenames_appliance(request):
    global root
    smp_suites = SimpleData()
    root_inv = os.path.join(root, 'inv')
    root_app = os.path.join(root_inv, 'appliance')
    # "C:/Users/pamid/PycharmProjects/djagoproject/robot/inv/appliance"
    files = os.listdir(root_app)
    # for path, dirs, files in os.walk(root_app):
    for files in files:
        if files.endswith('.py'):
            smp_suites.add(files)
    return Response(smp_suites.__dict__)


# async = asyncio_stream.ThreadPool(5)


def update_session_data(username, command, stime, etime, exe_session_id, server_port):
    # import pymysql
    #
    # cnx = pymysql.connect(host='localhost', user='root', password='Pamidi7997', db='mydatabase')
    # cursor = cnx.cursor()
    # exe_session_id = uuid.UUID
    # cursor.execute("insert into user_execution_session_log(username,command,starttime,endtime,exe_session_id)VALUES(%s,%s,%s,%s,%s)",('username','command',stime,etime,'exe_session_id')) # NOQA
    # # for i in cursor.fetchall():
    # #     print(i)
    # # Make sure data is committed to the database
    #
    # # data = {
    # #     'username': username,
    # #     'command':command,
    # #     'starttime': stime,
    # #     'endtime': etime,
    # #     'exe_session_id': exe_sesson_id,
    # # }
    # # data=(username,command,stime,etime,exe_sesson_id)
    # # cursor.execute(insert, data)
    # # Make sure data is committed to the database
    # cnx.commit()
    #
    # cursor.close()
    # cnx.close()
    # update from here
    # p = user_execution_session_log(username=username,command=command,sttime=stime, setime=datetime(etime),sessionexeid=exe_session_id) # NOQA
    p = user_execution_session_log()
    p.username = username
    p.command = command
    p.starttime = stime
    p.endtime = etime
    p.session_exe_id = exe_session_id
    p.save()
    global threader
    threader = asyncio_generator.Threader()  # .create_async_thread("ping google.com", exe_session_id, '')
    threader.create_thread(command, exe_session_id, server_port)


@api_view(['POST'])
# @parser_classes((JSONParser, ))
def get_options(request):
    global suser

    ststart = datetime.datetime.now(tz=timezone.utc)
    stout = request.session.get_expiry_date()

    username = request.session['username']

    # print(type(username))
    # print(type(ststart),type(stout))
    command = str(request.data)
    # session_id=request.session['username']

    stime = ststart
    etime = stout
    # cnx = pymysql.connect(host='localhost', user='root', password='Pamidi7997', db='mydatabase')
    # cursor = cnx.cursor()
    exe_session_id = uuid.uuid4().hex
    # print(type(exe_session_id),type(command))
    # cursor.execute(
    #     "INSERT INTO user_execution_session_log(username,command,starttime,endtime,exe_session_id)VALUES(%s,%s,%s,%s,%s)",(user, command, stime, etime, exe_session_id))  # NOQA
    # # for i in cursor.fetchall():
    # #     print(i)
    # # Make sure data is committed to the database
    #
    # # data = {
    # #     'username': username,
    # #     'command':command,
    # #     'starttime': stime,
    # #     'endtime': etime,
    # #     'exe_session_id': exe_sesson_id,
    # # }
    # # data=(username,command,stime,etime,exe_sesson_id)
    # # cursor.execute(insert, data)
    # # Make sure data is committed to the database
    # cnx.commit()
    #
    # cursor.close()
    # cnx.close()
    update_session_data(username, command, stime, etime, exe_session_id, server_port=request.META["SERVER_PORT"])
    return JsonResponse({'session_id': exe_session_id}, content_type="application/json")



@api_view(['GET'])
def history(request):
    if request.method == "POST":
        raise RuntimeError
    # if request.query_params.get('user') == None:
    #     raise RuntimeError("User not specified")
    # user = request.query_params.get('user')
    user = request.session['username']
    data = user_execution_session_log.objects.filter(username=user)
    # for item in data:
    #     username=item.username
    #     command=item.command
    # return Response(username,command)
    data_dic = []
    for item in data:
        sub_dic = {}
        sub_dic['username'] = item.username
        sub_dic['command'] = item.command
        sub_dic['starttime'] = item.starttime
        sub_dic['endtime'] = item.endtime
        sub_dic['session_exe_id'] = item.session_exe_id
        data_dic.append(sub_dic)
    # return JsonResponse({'result':data_dic}, content_type="application/json")
    return Response(data_dic)


@api_view(['GET'])
def update_message(request):
    sessionid = request.query_params.get('sessionid')
    message = request.query_params.get('message')

    p = test_execution_log()
    p.message = message
    p.session_id = sessionid
    p.save()
    return HttpResponse("")


@api_view(['POST'])
def log_stream(request):
    if request.method == "GET":
        raise RuntimeError
    # Raise bad response on illegal request
    if request.META.get('HTTP_COUNT', '-1') == '-1' or request.META.get('HTTP_COUNT', '-1').isdigit() is False \
            or request.META.get('HTTP_SESSIONID', '-1') == '-1':
        return HttpResponse(status='400')
    count = request.META.get('HTTP_COUNT', '-1')
    sessionid = request.META.get('HTTP_SESSIONID', '-1')
    now = timezone.now()
    if test_execution_log.objects.filter(session_id=sessionid).exists():
        resultset = test_execution_log.objects.filter(Q(session_id=sessionid) & Q(timestamp__lt=now)).values('message')
        # print(resultset.query)
        data = []
        for item in resultset:
            data.append(item['message'])

        return JsonResponse({'result': data[int(count):], 'count': len(data) - 1}, content_type="application/json")
    else:
        return HttpResponse(status=404)
