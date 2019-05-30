from django.http.response import JsonResponse
from django.shortcuts import render_to_response
import time

def cmpwind(s1,s2): # 0是小于，1是等于，2是大于
    if s1 == s2 :
        return 1
    elif s1 == 'low' :
        return 0
    elif s1 == 'mid' :
        if s2 == 'low' :
            return 2
        else :
            return 0
    else :
        return 2

def feecalc(s): #根据风速求费率
    if s == 'low' :
        return 0.25
    elif s == 'mid' :
        return 0.5
    else:
        return 0.75

class conditioner:
    def __init__(self):
        self.powe_on = 0
        self.start_up = 0

host = conditioner()

def powerOn ():
    response = {}
    host.powr_on = 1
    response['state'] = 'ok'
    return JsonResponse(response)

def setPara(request):
    response = {}
    if request.POST:
        host.mode = request.POST['model']
        host.tempHighLimit = request.POST['temp_high_limit']
        host.tempLowLimit = request.POST['temp_low_limit']
        host.targetTemp = request.POST['default_target_temp']
        host.feeRateH = request.POST['fee_rate_h']
        host.feeRateM = request.POST['fee_rate_m']
        host.feeRateL = request.POST['fee_rate_l']
        host.numRooms = request.POST['num_rooms']
        host.numServe = request.POST['num_serve']
        response['state'] = 'ok'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def startUp():
    response = {}
    host.start_up = 1
    response['state'] = 'ok'
    return JsonResponse(response)

class room:
    def __init__(self,roomid):
        self.roomid = roomid
        self.isCheckIn = 0
        self.isOpen = 0
        self.isServing = 0
        self.currentTemp = 27
        #dispatchid
        #serviceid

    def printRDR(self,request): #打印详单
        response = {}
        return JsonResponse(response)

    def printInvoice(self,request): #打印账单
        response = {}
        return JsonResponse(response)

roomlist = {}

class dispatch:
    dispatchcount = 0
    def __init__(self,roomid,wind,temp,fee_rate,mode):
        dispatch.dispatchcount += 1
        self.id = dispatch.dispatchcount
        self.roomid = roomid
        self.wind = wind
        self.target_temp = temp
        self.fee_rate = fee_rate
        self.fee = 0
        self.mode = mode
        #waittime
        #waitclock
        #serviceid

servicelist = {} #调度对象的服务队列
waitlist = {} #调度对象的等待队列

class serviceobj:
    servicecount = 0
    def __init__(self,roomid):
        serviceobj.servicecount += 1
        self.id = serviceobj.servicecount
        self.roomid = roomid
        self.status = 0
        self.clock = time.time() #服务开始时间
        #dispatchid
        
serviceobjlist = {} #服务对象队列

def checkRoomState(request): #查看房间状态
    response = {}
    if request.POST:
        roomid = request.POST['room_id']
        if not (roomlist.__contains__(roomid)):
            roomlist[roomid] = room(roomid)
        response['isCheckIn'] = roomlist[roomid].isCheckIn
        response['isOpen'] = roomlist[roomid].isOpen
        response['current_temp'] = roomlist[roomid].currentTemp
        if roomlist[roomid].isOpen == 1:
            response['isServing'] = roomlist[roomid].isServing
            obj = 0
            if servicelist.__contains__(roomlist[roomid].dispatchid) :
                obj = servicelist[roomlist[roomid].dispatchid]
            else:
                obj = waitlist[roomlist[roomid].dispatchid]
            response['wind'] = obj.wind
            response['target_temp'] = obj.target_temp
            response['fee_rate'] = obj.fee_rate
            response['fee'] = obj.fee
        response['state'] = 'ok'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def changeTargetTemp(request): #顾客更改空调目标温度
    response = {}
    if request.POST:
        roomid = request.POST['room_id']
        temp = request.POST['target_temp']
        if roomlist.__contains__(roomid):
            if roomlist[roomid].isServing == 1 :
                servicelist[roomlist[roomid].dispatchid].target_temp = temp
            else:
                waitlist[roomlist[roomid].dispatchid].target_temp = temp
            response['state'] = 'ok'
        else:
            response['state'] = 'fail'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def changeFanSpeed(request): #顾客更改空调风速
    response = {}
    if request.POST:
        roomid = request.POST['room_id']
        fan = request.POST['fan_speed']
        if roomlist.__contains__(roomid):
            if roomlist[roomid].isServing == 1 :
                servicelist[roomlist[roomid].dispatchid].wind = fan
                servicelist[roomlist[roomid].dispatchid].fee_rate = feecalc(fan)
            else:
                waitlist[roomlist[roomid].dispatchid].wind = fan
                waitlist[roomlist[roomid].dispatchid].fee_rate = feecalc(fan)
            response['state'] = 'ok'
        else:
            response['state'] = 'fail'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def requestOn(request): #顾客请求开机
    response = {}
    if request.POST:
        roomid = request.POST['room_id']
        obj = dispatch(roomid,'low',27,0.25,'cold') #调度
        if not roomlist.__contains__(roomid):
            roomlist[roomid] = room(roomid)
        roomlist[roomid].isCheckIn = 1
        roomlist[roomid].isOpen = 1
        roomlist[roomid].currentTemp = request.POST['current_room_temp']
        roomlist
        if len(servicelist)<host.numServe: #直接进入服务
            servicelist[obj.id] = obj
            serviceobject = serviceobj(roomid)
            obj.serviceid = serviceobject.id
            serviceobject.dispatchid = obj.id
            roomlist[roomid].serviceid = serviceobject.id
            roomlist[roomid].dispatchid = obj.id
            roomlist[roomid].isServing = 1
            serviceobject.status = 1
            serviceobjlist[serviceobject.id] = serviceobject
        else:
            flag = True
            for i in serviceobjlist:
                if flag:
                    target = i
                    flag = False
                else:
                    if cmpwind(target.wind , i.wind) == 2 :
                        target = i
                    elif cmpwind(target.wind , i.wind) == 1 :
                        if target.clock > i.clock :
                            target = i
            if cmpwind('low' , target.wind) == 0: #从队中挤出一个
                del serviceobjlist[target.id]
                obj2 = servicelist[target.dispatchid]
                del servicelist[obj2]
                waitlist[obj2.id] = obj2
                obj2.waitclock = time.time()
                obj2.waittime = 2
                roomlist[target.roomid].isServing = 0
                servicelist[obj.id] = obj
                serviceobject = serviceobj(roomid) #新建一个服务对象
                obj.serviceid = serviceobject.id
                serviceobject.dispatchid = obj.id
                roomlist[roomid].isServing = 1
                serviceobject.status = 1
                serviceobjlist[serviceobject.id] = serviceobject
            elif cmpwind('low' , target.wind) == 1: #进入等待队列
                waitlist[obj.id] = obj
                obj.waitclock = time.time()
                obj.waittime = 2
            else:
                waitlist[obj.id] = obj
                obj.waitclock = time.time()
                obj.waittime = -1
        response['modele'] = roomlist[roomid].mode
        response['target_temp'] =  roomlist[roomid].targetTemp
        response['temp_high_limit'] = host.tempHighLimit
        response['temp_low_limit'] = host.tempLowLimit
        response['state'] = 'ok'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def requestOff(request): #顾客关机
    response = {}
    if request.POST:
        roomid = request.POST['roomid']
        roomlist[roomid].currentTemp = request.POST['current_room_temp']
        dispatchid = roomlist[roomid].dispatchid
        roomlist[roomid].dispatchid = 0
        roomlist[roomid].isOpen = 0
        if servicelist.__contains__(dispatchid) :
            del servicelist[dispatchid]
        else:
            del waitlist[dispatchid]
        if roomlist[roomid].isServing == 1 :
            serviceid = roomlist[roomid].serviceid
            roomlist[roomid].serviceid = 0
            roomlist[roomid].isServing = 0
            del serviceobjlist[serviceid]
        response['state'] = 'ok'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def requestInfo(request): #每分钟查看一次费用
    response = {}
    return JsonResponse(response)

def printReport(request): #打印报表
    response = {}
    return JsonResponse(response)