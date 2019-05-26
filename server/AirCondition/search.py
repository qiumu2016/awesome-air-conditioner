from django.http.response import JsonResponse
from django.shortcuts import render_to_response

class conditioner:
    def __init__(self):
        self.mode = 'cold'
        self.tempHighLimit = 30
        self.tempLowLimit = 10
        self.defaultTargetTemp = 20
        self.feeRateH = 0.75
        self.feeRateM = 0.5
        self.feeRateL = 0.25
        self.numRooms = 4
        self.numServe= 3

    def startUp(self):
        response = {}
        response['state'] = 'ok'
        return JsonResponse(response)

    def setPara(self):
        response = {}
        self.startUp()
        response['state'] = 'ok'
        return JsonResponse(response)

    def powerOn (self):
        response = {}
        self.setPara()
        response['state'] = 'ok'
        return JsonResponse(response)

class room:
    def __init__(self,roomid):
        self.roomid = roomid
        self.isCheckIn = 0
        self.isOpen = 0
        self.isServing = 0
        self.wind = 'low'
        self.currentTemp = 27
        self.targetTemp = 27
        self.feeRate= 0.25
        self.fee = 0

    def checkRoomState(self,request):
        response = {}
        return JsonResponse(response)

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









def queryReport(self,request):
    response = {}
    return JsonResponse(response)

def printReport(self,request):
    response = {}
    return JsonResponse(response)