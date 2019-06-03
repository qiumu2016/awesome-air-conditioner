from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.http import HttpResponse

from . import search

class PowerOnView(APIView):
    def post(self, request):
        response = search.host.powerOn()
        return response

class SetParaView(APIView):
    def post(self, request):
        response = search.host.setPara(request)
        return response

class StartUpView(APIView):
    def post(self, request):
        response = search.host.startUp()
        return response

class CheckRoomStateView(APIView):
    def post(self, request):
        response = search.checkRoomState(request)
        return response

class PrintRDRView(APIView):
    def post(self, request):
        response = search.room.printRDR(request)
        return response

class PrintInvoiceView(APIView):
    def post(self, request):
        response = search.printInvoice(request)
        return response

class PrintReportView(APIView):
    def post(self, request):
        response = search.printReport(request)
        return response
    
class RequestOnView(APIView):
    def post(self, request):
        response = search.requestOn(request)
        return response

class RequestOffView(APIView):
    def post(self, request):
        response = search.requestOff(request)
        return response

class ChangeTargetTempView(APIView):
    def post(self, request):
        response = search.changeTargetTemp(request)
        return response

class ChangeFanSpeedView(APIView):
    def post(self, request):
        response = search.changeFanSpeed(request)
        return response

class RequestInfoView(APIView):
    def post(self, request):
        response = search.requestInfo(request)
        return response
