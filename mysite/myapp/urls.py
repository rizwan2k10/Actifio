from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from .views import register, user_login,\
    user_logout, filenames_host, filenames_testcases, filenames_appliance, get_workspace, \
    get_options, history, log_stream, update_message, home
urlpatterns = [

    url(r'^home.html', home),
    # url(r'^commands', update_session_data),
    url(r'^getoptions', get_options),
    url(r'^root/', get_workspace),
    url(r'^host/', filenames_host),
    url(r'^testcases/', filenames_testcases),
    url(r'^appliance/', filenames_appliance, name='appliance'),
    url(r'^actifio/', user_login, name='user_login'),
    # url(r'^hello/', hello_world),
    url(r'^register/', register),
    url(r'^logout/', user_logout),
    url(r'^history/', history),
    url(r'^execution', log_stream),
    url(r'^update_log', update_message),
]