from django.http.response import JsonResponse
from django.shortcuts import render_to_response
from conditioner import conditioner

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

def powerOn (self, request):
    response = {}
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