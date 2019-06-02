from django.http.response import JsonResponse
from django.shortcuts import render_to_response
import time
import datetime
import sqlite3
import string

dbpath = 'db [2]'

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
        return 0.3
    elif s == 'mid' :
        return 0.5
    else:
        return 1

class conditioner:
    def __init__(self):
        self.power_on = 0
        self.start_up = 0

host = conditioner()

def powerOn ():
    response = {}
    host.power_on = 1
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
        self.dispatchid = 0
        self.serviceid = 0

    def printRDR(self,request): #打印详单
        response = {}
        if request.POST:
            roomid = request.POST['room_id']
            dateIn = request.POST['date_in']
            dateOut = request.POST['date_out']

            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()
            queryDetailSql = '''select room_id, start_time, (end_time - start_time), wind, fee_rate, fee
                                from AirCondition_details
                                where room_id = ? and start_time >= ? and end_time <= ?
            '''
            cursor.execute(queryDetailSql, (roomid, dateIn, dateOut))
            values = cursor.fetchall()
            valuesStr = "".join(values)
            cursor.close()
            conn.close()

            mode = 'RDR_{}'
            with open(mode.format(roomid) + '.txt', 'a', encoding='utf-8') as f:
                f.write(valuesStr)

            response['state'] = 'ok'
        else:
            response['state'] = 'fail'
        return JsonResponse(response)

    def printInvoice(self,request): #打印账单
        response = {}
        if request.POST:
            roomid = request.POST['room_id']
            dateIn = request.POST['date_in']
            dateOut = request.POST['date_out']
            self.isCheckIn = 0
            dispatchid = self.dispatchid
            if waitlist.__contains__(dispatchid) :
                del waitlist[dispatchid]
            else:
                del servicelist[dispatchid]
            serviceid = self.serviceid
            del serviceobjlist[serviceid]

            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()
            queryDetailSql = '''select sum(fee)
                                from AirCondition_details
                                where room_id = ? and start_time >= ? and end_time <= ?
            '''
            cursor.execute(queryDetailSql, (roomid, dateIn, dateOut))
            values = cursor.fetchone()
            valuesStr = "".join(values)
            cursor.close()
            conn.close()

            mode = 'Invoice_{}'
            with open(mode.format(roomid) + '.txt', 'a', encoding='utf-8') as f:
                f.write(valuesStr)

            response['state'] = 'ok'
        else:
            response['state'] = 'fail'
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
        self.feeprogress = 0
        #waittime
        #waitclock
        #serviceid
        #feeprogress

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

        connR = sqlite3.connect(dbpath)
        cursorR = connR.cursor()
        updateReportSql = '''update AirCondition_report
                             set schedule = schedule + 1, change_temp = change_temp + 1
                             where room_id = ?
        '''
        cursorR.execute(updateReportSql, roomid)
        cursorR.close()
        connR.commit()
        connR.close()
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def changeFanSpeed(request): #顾客更改空调风速
    response = {}
    t2 = datetime.datetime.now()
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

            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()
            queryDetailSql1 = '''select MAX(id)
                                 from AirCondition_details
                                 where room_id = ?
            '''
            cursor.execute(queryDetailSql1, roomid)
            updateId = cursor.fetchone()
            queryDetailSql2 = '''select check_in_time
                                 from AirCondition_details
                                 where room_id = ?
            '''
            cursor.execute(queryDetailSql2, roomid)
            t1 = cursor.fetchone()
            s1 = t1.strftime("%Y%m%d%H%M%S")
            i1 = int(s1)
            s2 = t2.strftime("%Y%m%d%H%M%S")
            i2 = int(s2)
            addFee = (i2 - i1) * feecalc(fan) / 60
            temp1 = roomlist[roomid].currentTemp

            updateDetailSql = '''update AirCondition_details
                                 set end_time = ?, end_temp = ?,fee = ?
                                 where id = ?
            '''
            cursor.execute(updateDetailSql, (t2, temp1, addFee, updateId))


            addDetailSql = '''insert into AirCondition_details
                              (check_in_time, room_id, model, operation, start_time, start_temp, wind, fee_rate)
                              values 
                              (?, ?, ?, ?, ?, ?, ?, ?)
            '''

            cursor.execute(addDetailSql, (t1, roomid, 'cold', 'fan', t2, temp1, fan, feecalc(fan)))
            cursor.close()
            conn.commit()
            conn.close()


            connR = sqlite3.connect(dbpath)
            cursorR = connR.cursor()
            updateReportSql = '''update AirCondition_report
                                 set time = time + ?, schedule = schedule + 1, change_wind = change_wind + 1
                                 where room_id = ?
            '''
            cursorR.execute(updateReportSql, ((i2 - i1), roomid))
            cursorR.close()
            connR.commit()
            connR.close()

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
        obj = dispatch(roomid,'mid',host.targetTemp,0.5,'cold') #调度
        if not roomlist.__contains__(roomid):
            roomlist[roomid] = room(roomid)
        if roomlist[roomid].isCheckIn == 0:
            roomlist[roomid].isCheckIn = 1
            roomlist[roomid].checkInTime = datetime.datetime.now()
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
            if cmpwind('mid' , target.wind) == 0: #从队中挤出一个
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
            elif cmpwind('mid' , target.wind) == 1: #进入等待队列
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

    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    addDetailSql = '''insert into AirCondition_details
                      (check_in_time, room_id, model, operation, start_time, start_temp, wind, fee_rate)
                      values
                      (?, ?, 'cold', 'start', ?, 27, 'low', 0.25)
    '''
    cursor.execute(addDetailSql, (t1, roomid, t1))
    cursor.close()
    conn.commit()
    conn.close()

    connR = sqlite3.connect(dbpath)
    cursorR = connR.cursor()
    queryReportSql = '''select id
                        from AirCondition_report
                        where room_id = ?
    '''
    cursorR.execute(queryReportSql, roomid)
    idR = cursorR.fetchone()
    if (idR == None):
        addReportSql = '''insert into AirCondition_report
                          (room_id, switch, time, fee, schedule, change_temp, change_wind) 
                          values 
                          (?, 1, 0, 0, 1, 0, 0)
        '''
        cursorR.execute(addReportSql, roomid)
    else:
        updateReportSql = '''update AirCondition_report
                             set switch = switch + 1
                             where id = ?
        '''
        cursorR.execute(updateReportSql, idR)
    cursorR.close()
    connR.commit()
    connR.close()

    return JsonResponse(response)

def requestOff(request): #顾客关机
    response = {}
    t2 = datetime.datetime.now()
    if request.POST:
        roomid = request.POST['room_id']

        #
        feerate = feecalc(roomlist[roomid].wind)
        #

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

        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        queryDetailSql1 = '''select MAX(id)
                             from AirCondition_details
                             where room_id = ?
        '''
        cursor.execute(queryDetailSql1, roomid)
        updateId = cursor.fetchone()
        queryDetailSql2 = '''select check_in_time
                             from AirCondition_details
                             where room_id = ?
        '''
        cursor.execute(queryDetailSql2, roomid)
        t1 = cursor.fetchone()
        s1 = t1.strftime("%Y%m%d%H%M%S")
        i1 = int(s1)
        s2 = t2.strftime("%Y%m%d%H%M%S")
        i2 = int(s2)
        addFee = (i2 - i1) * feecalc(roomlist[roomid].wind)
        temp1 = roomlist[roomid].currentTemp

        updateDetailSql = '''update AirCondition_details
                             set end_time = ?, end_temp = ?,fee = ?
                             where id = ?
        '''
        cursor.execute(updateDetailSql, (t2, temp1, addFee, updateId))
        cursor.close()
        conn.commit()
        conn.close()


        connR = sqlite3.connect(dbpath)
        cursorR = connR.cursor()
        updateReportSql = '''update AirCondition_report
                             set time = time + ? , fee = fee + ?
                             where room_id = ?
        '''
        cursorR.execute(updateReportSql, ((i2 - i1), roomid, (i2 - i1) * feerate))
        cursorR.close()
        connR.commit()
        connR.close()

    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def requestInfo(request): #每分钟查看一次费用
    response = {}
    if request.POST:
        roomid = request.POST['room_id']
        if roomlist.__contains__(roomid) :
            response['isCheckIn'] = roomlist[roomid].isCheckIn
            response['isOpen'] = roomlist[roomid].isOpen
            response['isServing'] = roomlist[roomid].isServing
            obj = 0
            if servicelist.__contains__(roomlist[roomid].dispatchid) :
                obj = servicelist[roomlist[roomid].dispatchid]
            else:
                obj = waitlist[roomlist[roomid].dispatchid]
            response['wind'] = obj.wind
            response['current_temp'] = roomlist[roomid].currentTemp
            response['fee_rate'] = obj.fee_rate
            response['fee'] = obj.fee
            response['state'] = 'ok'
        else:
            response['state'] = 'fail'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def printReport(request): #打印报表
    response = {}
    if request.POST:
        roomid = request.POST['room_id']
        connR = sqlite3.connect(dbpath)
        cursorR = connR.cursor()
        queryReportSql = '''select *
                            from AirCondition_report
                            where room_id = ?
        '''
        cursorR.execute(queryReportSql,roomid)
        values = cursorR.fetchall()
        valuesStr = "".join(values)
        cursorR.close()
        connR.close()

        mode = 'Report_{}'
        with open(mode.format(roomid) + '.txt', 'a', encoding='utf-8') as f:
            f.write(valuesStr)

        response['state'] = 'ok'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)