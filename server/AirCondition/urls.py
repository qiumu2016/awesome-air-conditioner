from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    #administrator
    url(r'^power_on/$', views.PowerOnView.as_view()),
    url(r'^set_para/$', views.SetParaView.as_view()),
    url(r'^start_up/$', views.StartUpView.as_view()),
    url(r'^check_room_state/$', views.CheckRoomStateView.as_view()),
    #desk
    url(r'^print_rdr/$', views.PrintRDRView.as_view()),
    url(r'^print_invoice/$', views.PrintInvoiceView.as_view()),
    #manager
    url(r'^print_report/$', views.PrintReportView.as_view()),
    #customer
    url(r'^request_on/$', views.RequestOnView.as_view()),
    url(r'^request_off/$', views.RequestOffView.as_view()),
    url(r'^change_target_temp/$', views.ChangeTargetTempView.as_view()),
    url(r'^change_fan_speed/$', views.ChangeFanSpeedView.as_view()),
    url(r'^request_info/$', views.RequestInfoView.as_view()),
]