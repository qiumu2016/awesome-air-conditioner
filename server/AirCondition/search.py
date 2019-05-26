from django.http.response import JsonResponse
from django.shortcuts import render_to_response

class conditioner:
    def __init__(self,Mode,Temp_highLimit,Temp_lowLimit,default_TargetTemp,FeeRate_H,FeeRate_M,FeeRate_L):
        self.Mode = Mode
        self.Temp_highLimit = 30
        self.Temp_lowLimit = 10
        self.default_TargetTemp = 20
        self.FeeRate_H = 0.75
        self.FeeRate_M = 0.5
        self.FeeRate_L = 0.25

def requestOn(self,request):
    response = {}
    return JsonResponse(response)

def changeTargetTemp(self,request):
    response = {}
    return JsonResponse(response)

def changeFanSpeed(self,request):
    response = {}
    return JsonResponse(response)

def requestOff(self,request):
    response = {}
    return JsonResponse(response)

def requestFee(self,request):
    response = {}
    return JsonResponse(response)

def createRDR(self,request):
    response = {}
    return JsonResponse(response)

def printRDR(self,request):
    response = {}
    return JsonResponse(response)

def createInvoice(self,request):
    response = {}
    return JsonResponse(response)

def printInvoice(self,request):
    response = {}
    return JsonResponse(response)

def powerOn ():
    response = {}
    response['state'] = 'ok'
    return JsonResponse(response)

def setPara(self,request):
    response = {}
    return JsonResponse(response)

def startUp(self,request):
    response = {}
    return JsonResponse(response)

def checkRoomState(self,request):
    response = {}
    return JsonResponse(response)

def queryReport(self,request):
    response = {}
    return JsonResponse(response)

def printReport(self,request):
    response = {}
    return JsonResponse(response)