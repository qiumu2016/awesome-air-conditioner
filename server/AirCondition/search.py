from django.http.response import JsonResponse
from django.http import FileResponse  
from django.shortcuts import render_to_response
import time
import datetime
import sqlite3
import string
import os
import json
import threading

dbpath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db.sqlite3')

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

class conditioner:
    def __init__(self):
        self.power_on = 0
        self.start_up = 0
        self.targetTemp = 0
        self.feeRateH = 0
        self.feeRateL = 0
        self.feeRateM = 0
        self.numServe = 0

    def startUp(self):
        response = {}
        self.start_up = 1
        self.timer = threading.Timer(1.0,self._update)
        self.timer.start()
        response['state'] = 'ok'
        return JsonResponse(response)
    
    def powerOn (self):
        response = {}
        self.power_on = 1
        response['state'] = 'ok'
        return JsonResponse(response)
    
    def setPara(self,request):
        response = {}
        request_post = json.loads(request.body)
        if request_post:
            self.mode = request_post['model']
            self.tempHighLimit = request_post['temp_high_limit']
            self.tempLowLimit = request_post['temp_low_limit']
            self.targetTemp = request_post['default_target_temp']
            self.feeRateH = request_post['fee_rate_h']
            self.feeRateM = request_post['fee_rate_m']
            self.feeRateL = request_post['fee_rate_l']
            self.numRooms = request_post['num_rooms']
            self.numServe = request_post['num_serve']
            response['state'] = 'ok'
        else:
            response['state'] = 'fail'
        return JsonResponse(response)
    
    def _update(self):
        roomUpdate()
        self.timer = threading.Timer(1.0,self._update)
        self.timer.start()

host = conditioner()

def feecalc(s): #根据风速求费率
    if s == 'low' :
        return host.feeRateL
    elif s == 'mid' :
        return host.feeRateM
    else:
        return host.feeRateH

class room:
    def __init__(self,roomid):
        self.roomid = roomid
        self.isCheckIn = 0
        self.isOpen = 0
        self.isServing = 0
        self.currentTemp = 27.0
        self.checkInTime = 0
        self.fee = 0.0
        self.service = serviceobj(roomid)
        self.wind = 'mid'
        self.target_temp = host.targetTemp
        self.fee_rate = feecalc('mid')
        self.dispatchfee = 0.0
        self.mode = 'cold'
        #waittime
        #waitclock

    def printRDR(self,request): #打印详单
        #response = {}
        request_post = json.loads(request.body)
        if request_post:
            roomid = request_post['room_id']
            #dateIn = request_post['date_in']
            #dateOut = request_post['date_out']

            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()
            queryDetailSql = '''select room_id, start_time, (end_time - start_time), wind, fee_rate, fee
                                from AirCondition_details
                                where room_id = ? and check_in_time = ?
            '''
            cursor.execute(queryDetailSql, (int(roomid),roomlist[str(roomid)].checkInTime))
            values = cursor.fetchall()
            cursor.close()
            conn.close()

            valuesStr = str(values)
            printStr = 'RoomId,Time,Duration,FanSpeed,FeeRate,Fee\n'
            for i in range(len(valuesStr)):
                if (valuesStr[i] == '('):
                    for j in range(i,len(valuesStr)):
                        if(valuesStr[j] == ')'):
                            printStr = printStr + valuesStr[i + 1 : j] + '\n'
                            break
            printMode = 'RDR_{}'
            filename = printMode.format(roomid) + '.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(printStr)

            file=open(filename, 'rb')
            response =FileResponse(file)
            response['Content-Type']='application/octet-stream'
            response['Content-Disposition']='attachment;filename="{0}"'.format(filename)

            #response['state'] = 'ok'
        else:
            #response['state'] = 'fail'
            print('RDR FAILED')
        return response
        #return JsonResponse(response)


roomlist = {} #房间
servicelist = {} #调度对象的服务队列
waitlist = {} #调度对象的等待队列

class serviceobj:
    servicecount = 0
    def __init__(self,roomid):
        serviceobj.servicecount += 1
        self.id = serviceobj.servicecount
        self.roomid = roomid
        self.clock = time.time() #服务开始时间

def checkRoomState(request): #查看房间状态
    response = {}
    request_post = json.loads(request.body)
    if request_post:
        roomid = request_post['room_id']
        if not (roomlist.__contains__(roomid)):
            roomlist[str(roomid)] = room(roomid)
        response['isCheckIn'] = roomlist[str(roomid)].isCheckIn
        response['isOpen'] = roomlist[str(roomid)].isOpen
        response['current_temp'] = roomlist[str(roomid)].currentTemp
        response['isServing'] = roomlist[str(roomid)].isServing
        if roomlist[str(roomid)].isOpen == 1:
            response['wind'] = roomlist[str(roomid)].wind
            response['target_temp'] = roomlist[str(roomid)].target_temp
            response['fee_rate'] = roomlist[str(roomid)].fee_rate
            response['fee'] = roomlist[str(roomid)].fee
        response['state'] = 'ok'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def changeTargetTemp(request): #顾客更改空调目标温度
    response = {}
    request_post = json.loads(request.body)
    if request_post:
        roomid = request_post['room_id']
        temp = request_post['target_temp']
        if roomlist.__contains__(str(roomid)):
            roomlist[str(roomid)].target_temp = temp
            response['state'] = 'ok'
        else:
            response['state'] = 'fail'

        connR = sqlite3.connect(dbpath)
        cursorR = connR.cursor()
        updateReportSql = '''update AirCondition_report
                             set schedule = schedule + 1, change_temp = change_temp + 1
                             where room_id = ?
        '''
        cursorR.execute(updateReportSql, (int(roomid),))
        cursorR.close()
        connR.commit()
        connR.close()
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def changeFanSpeed(request): #顾客更改空调风速
    response = {}
    request_post = json.loads(request.body)
    if request_post:
        roomid = request_post['room_id']
        fan = request_post['fan_speed']
        if roomlist.__contains__(str(roomid)):
            roomlist[str(roomid)].wind = fan
            roomlist[str(roomid)].fee_rate = feecalc(fan)
            
            detailCheckInTime = roomlist[str(roomid)].checkInTime
            detailModel = roomlist[str(roomid)].mode
            detailCurrentTemp = roomlist[str(roomid)].currentTemp
            detailWind = roomlist[str(roomid)].wind
            detailFeeRate = roomlist[str(roomid)].fee_rate
            detailFee = roomlist[str(roomid)].dispatchfee
            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()
            queryDetailSql1 = '''select MAX(id)
                                 from AirCondition_details
                                 where room_id = ?
            '''
            cursor.execute(queryDetailSql1, (int(roomid),))
            t2 = datetime.datetime.now()
            updateId = cursor.fetchone()
            updateIdStr = str(updateId)[1:-2]
            if (updateId != None):
                updateDetailSql1 = '''update AirCondition_details
                                      set end_time = ?, end_temp = ?, fee = ?
                                      where id = ?
                '''
                cursor.execute(updateDetailSql1, (t2, detailCurrentTemp, detailFee, int(updateIdStr)))

            addDetailSql1 = '''insert into AirCondition_details
                               (check_in_time, room_id, model, operation, start_time, end_time, start_temp, end_temp, wind, fee_rate, fee)
                               values
                               (?, ?, ?, '0', ?, 0, ?, 0 ,?, ?, 0)
            '''
            cursor.execute(addDetailSql1, (detailCheckInTime, int(roomid), detailModel, t2, detailCurrentTemp, detailWind, detailFeeRate))
            t1 = roomlist[str(roomid)].checkInTime
            s1 = t1.strftime("%Y%m%d%H%M%S")
            i1 = int(s1)
            s2 = t2.strftime("%Y%m%d%H%M%S")
            i2 = int(s2)

            cursor.close()
            conn.commit()
            conn.close()

            connR = sqlite3.connect(dbpath)
            cursorR = connR.cursor()
            updateReportSql = '''update AirCondition_report
                                 set time = time + ?, fee = fee + ? ,schedule = schedule + 1, change_wind = change_wind + 1
                                 where room_id = ?
            '''
            cursorR.execute(updateReportSql, ((i2 - i1) / 60, detailFee, int(roomid)))
            cursorR.close()
            connR.commit()
            connR.close()

            response['state'] = 'ok'
            roomlist[str(roomid)].dispatchfee = 0.0
        else:
            response['state'] = 'fail'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def requestOn(request): #顾客请求开机
    response = {}
    request_post = json.loads(request.body)
    if request_post:
        roomid = request_post['room_id']
        if not roomlist.__contains__(roomid):
            roomlist[str(roomid)] = room(roomid)
        if roomlist[str(roomid)].isCheckIn == 0:
            roomlist[str(roomid)].isCheckIn = 1
            roomlist[str(roomid)].checkInTime = datetime.datetime.now()
        roomlist[str(roomid)].isOpen = 1
        roomlist[str(roomid)].currentTemp = float(request_post['current_room_temp'])
        if len(servicelist)<host.numServe: #直接进入服务
            servicelist[str(roomid)] = str(roomid)
            roomlist[str(roomid)].isServing = 1
        else:
            flag = True
            target = 0
            for i in servicelist.values():
                if flag:
                    target = i
                    flag = False
                else:
                    if cmpwind(roomlist[target].wind , roomlist[i].wind) == 2 :
                        target = i
                    elif cmpwind(roomlist[target].wind , roomlist[i].wind) == 1 :
                        if roomlist[target].service.clock > roomlist[i].service.clock :
                            target = i
            if cmpwind('mid' , roomlist[target].wind) == 0: #从队中挤出一个
                del servicelist[target]
                waitlist[target] = target
                target.waitclock = time.time()
                target.waittime = 120
                roomlist[target].isServing = 0
                servicelist[str(roomid)] = str(roomid)
                roomlist[str(roomid)].isServing = 1
            elif cmpwind('mid' , roomlist[target].wind) == 1: #进入等待队列
                waitlist[str(roomid)] = str(roomid)
                roomlist[str(roomid)].waitclock = time.time()
                roomlist[str(roomid)].waittime = 120
            else:
                waitlist[str(roomid)] = str(roomid)
                roomlist[str(roomid)].waitclock = time.time()
                roomlist[str(roomid)].waittime = -1
        response['modele'] = roomlist[str(roomid)].mode
        response['target_temp'] =  roomlist[str(roomid)].target_temp
        response['temp_high_limit'] = host.tempHighLimit
        response['temp_low_limit'] = host.tempLowLimit
        response['state'] = 'ok'

        connR = sqlite3.connect(dbpath)
        cursorR = connR.cursor()
        queryReportSql = '''select id
                            from AirCondition_report
                            where room_id = ?
        '''
        roomidInt = int(roomid)
        cursorR.execute(queryReportSql, (roomidInt,))
        idR = cursorR.fetchone()
        if (idR == None):
            addReportSql = '''insert into AirCondition_report
                              (room_id, switch, time, fee, schedule, change_temp, change_wind) 
                              values 
                              (?, 1, 0, 0, 1, 0, 0)
            '''
            cursorR.execute(addReportSql, (roomidInt,))
        else:
            updateReportSql = '''update AirCondition_report
                                 set switch = switch + 1
                                 where id = ?
            '''
            idR = str(idR)[1:-2]
            cursorR.execute(updateReportSql, (int(idR),))
        cursorR.close()
        connR.commit()
        connR.close()

    else:
        response['state'] = 'fail'

    return JsonResponse(response)

def requestOff(request): #顾客关机
    response = {}
    t2 = datetime.datetime.now()
    request_post = json.loads(request.body)
    if request_post:
        roomid = request_post['room_id']
        roomlist[str(roomid)].currentTemp = request_post['current_room_temp']
        roomlist[str(roomid)].isOpen = 0

        if servicelist.__contains__(str(roomid)) :
            del servicelist[str(roomid)]
        else:
            del waitlist[str(roomid)]
        if roomlist[str(roomid)].isServing == 1 :
            roomlist[str(roomid)].isServing = 0

        detailCurrentTemp = roomlist[str(roomid)].currentTemp
        detailFee = roomlist[str(roomid)].dispatchfee

        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        queryDetailSql1 = '''select MAX(id)
                             from AirCondition_details
                             where room_id = ?
        '''
        cursor.execute(queryDetailSql1, (int(roomid),))
        updateId = cursor.fetchone()
        updateIdStr = str(updateId)[1:-2]
        t1 = roomlist[str(roomid)].checkInTime
        s1 = t1.strftime("%Y%m%d%H%M%S")
        i1 = int(s1)
        s2 = t2.strftime("%Y%m%d%H%M%S")
        i2 = int(s2)

        updateDetailSql = '''update AirCondition_details
                             set end_time = ?, end_temp = ?,fee = ?
                             where id = ?
        '''
        cursor.execute(updateDetailSql, (t2, detailCurrentTemp, detailFee, int(updateIdStr),))
        cursor.close()
        conn.commit()
        conn.close()

        connR = sqlite3.connect(dbpath)
        cursorR = connR.cursor()
        updateReportSql = '''update AirCondition_report
                             set time = time + ? , fee = fee + ?
                             where room_id = ?
        '''
        cursorR.execute(updateReportSql, ((i2 - i1) / 60, detailFee, int(roomid),))
        cursorR.close()
        connR.commit()
        connR.close()

        roomlist[str(roomid)].dispatchfee = 0.0
        response['state'] = 'ok'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def requestInfo(request): #每分钟查看一次费用
    response = {}
    request_post = json.loads(request.body)
    if request_post:
        roomid = request_post['room_id']
        if roomlist.__contains__(roomid) :
            response['isCheckIn'] = roomlist[str(roomid)].isCheckIn
            response['isOpen'] = roomlist[str(roomid)].isOpen
            response['isServing'] = roomlist[str(roomid)].isServing
            response['current_temp'] = roomlist[str(roomid)].currentTemp
            if (roomlist[str(roomid)].isOpen == 1):
                response['wind'] = roomlist[str(roomid)].wind
                response['fee_rate'] = roomlist[str(roomid)].fee_rate
                response['fee'] = roomlist[str(roomid)].fee
            response['state'] = 'ok'
        else:
            response['state'] = 'fail'
    else:
        response['state'] = 'fail'
    return JsonResponse(response)

def printReport(request): #打印报表
    response = {}
    request_post = json.loads(request.body)
    if request_post:
        printTypeId = str(request_post['type'])
        if printTypeId == '0' :
            printType = 'Day'
        if printTypeId == '1' :
            printType = 'Week'
        if printTypeId == '2' :
            printType = 'Month'
        if printTypeId == '3' :
            printType = 'Year'
        connR = sqlite3.connect(dbpath)
        cursorR = connR.cursor()
        queryReportSql = '''select *
                            from AirCondition_report
        '''
        cursorR.execute(queryReportSql)
        values = cursorR.fetchall()
        cursorR.close()
        connR.close()

        valuesStr = str(values)
        printStr = 'Id,RoomId,TimesOfOnOff,Duration,TotalFee,TimesOFDispatch,TimesOfChangeTemp,TimesOfChangeFanSpeed\n'
        for i in range(len(valuesStr)):
            if (valuesStr[i] == '('):
                for j in range(i, len(valuesStr)):
                    if (valuesStr[j] == ')'):
                        printStr = printStr + valuesStr[i + 1: j] + '\n'
                        break

        printMode = 'Report_{}'
        filename = printMode.format(printType) + '.txt'
        with open(printMode.format(printType) + '.txt', 'w', encoding='utf-8') as f:
            f.write(printStr)

        file=open(filename, 'rb')
        response =FileResponse(file)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename="{0}"'.format(filename)

        #response['state'] = 'ok'
    else:
        #response['state'] = 'fail'
        print('REPORT FAILED')
    return response
    #return JsonResponse(response)

def printInvoice(request): #打印账单
    response = {}
    request_post = json.loads(request.body)
    if request_post:
        roomid = request_post['room_id']
        roomlist[str(roomid)].isCheckIn = 0
        roomlist[str(roomid)].fee = 0
        dispatchid = roomlist[str(roomid)].dispatchid
        if waitlist.__contains__(dispatchid) :
            del waitlist[dispatchid]
        elif servicelist.__contains__(dispatchid) :
            del servicelist[dispatchid]

        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        queryDetailSql = '''select sum(fee)
                            from AirCondition_details
                            where room_id = ?
        '''
        cursor.execute(queryDetailSql, (int(roomid),))
        values = cursor.fetchone()
        valuesStr = str(values)[1:-2]
        cursor.close()
        conn.close()

        printStr = 'RoomId,Fee/yuan\n'
        printMode = 'Invoice_{}'
        filename = printMode.format(roomid) + '.txt'
        with open(printMode.format(roomid) + '.txt', 'w', encoding='utf-8') as f:
            f.write(printStr + str(roomid) + ',' + valuesStr)

        file=open(filename, 'rb')
        response =FileResponse(file)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename="{0}"'.format(filename)

        #response['state'] = 'ok'
    else:
        #response['state'] = 'fail'
        print('REPORT FAILED')
    return response
    #return JsonResponse(response)

def roomUpdate():
    for j in roomlist:#正在空调服务的房间空调变化
        if roomlist[j].isServing == 1:
            temp = roomlist[j].fee_rate / 60.0
            roomlist[j].fee += temp
            roomlist[j].dispatchfee += temp
            if roomlist[j].mode == 'cold' :
                temp = 0.0 - temp
            print(j)
            roomlist[j].currentTemp += temp
            if (roomlist[j].mode == 'hot' and roomlist[j].currentTemp >= roomlist[j].target_temp) or (roomlist[j].mode == 'cold' and roomlist[j].currentTemp <= roomlist[j].target_temp) : #服务结束
            #服务结束 
                roomlist[j].currentTemp = roomlist[j].target_temp
                roomlist[j].isOpen = 0
                roomlist[j].isServing = 0
                
                t2 = datetime.datetime.now()
                detailCurrentTemp = roomlist[j].currentTemp
                detailFee = roomlist[j].dispatchfee

                conn = sqlite3.connect(dbpath)
                cursor = conn.cursor()
                queryDetailSql = '''select MAX(id)
                                    from AirCondition_details
                                    where room_id = ?
                '''
                cursor.execute(queryDetailSql,(int(j),))
                updateIdList = cursor.fetchone()
                updateIdStr = str(updateIdList)[1:-2]
                updateId = int(updateIdStr)
                updateDetailSql = '''update AirCondition_details
                                     set end_time = ?, end_temp = ?, fee = ?
                                     where id = ?
                '''
                cursor.execute(updateDetailSql, (t2, detailCurrentTemp, detailFee, updateId,))

                cursor.close()
                conn.commit()
                conn.close()

                roomlist[j].dispatchfee = 0.0
                del servicelist[j]

    for i in waitlist.values() : #等待队列的等待时间减一
        roomlist[i].waittime -= 1
        if roomlist[i].waittime == 0: #已经到时，强行入队
            flag = True 
            target = 0
            for j in servicelist.values() :
                if flag :
                    flag = False
                    target = j
                else:
                    if roomlist[target].service.clock > roomlist[j].service.clock :
                        target = j
            del servicelist[target]
            waitlist[target] = target
            roomlist[target].waitclock = time.time()
            roomlist[target].waittime = 120
            roomlist[target].isServing = 0
            del waitlist[i]
            servicelist[i] = i
            roomlist[i].isServing = 1

            t2 = datetime.datetime.now()
            detailCurrentTemp1 = roomlist[target].currentTemp
            detailFee1 = roomlist[target].dispatchfee

            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()
            queryDetailSql = '''select MAX(id)
                                from AirCondition_details
                                where room_id = ?
            '''
            cursor.execute(queryDetailSql, (int(target),))
            updateIdList = cursor.fetchone()
            updateIdStr = str(updateIdList)[1:-2]
            updateId = int(updateIdStr)
            updateDetailSql = '''update AirCondition_details
                                 set end_time = ?, end_temp = ?, fee = ?
                                 where id = ?
             '''
            cursor.execute(updateDetailSql, (t2, detailCurrentTemp1, detailFee1, updateId,))

            detailCheckInTime2 = roomlist[i].checkInTime
            detailModel2 = roomlist[i].mode
            detailStartTime2 = t2
            detailStartTemp2 = roomlist[i].currentTemp
            detailWind2 = roomlist[i].wind
            detailFeeRate2 = roomlist[i].fee_rate
            addDetailSql = '''insert into AirCondition_details
                              (check_in_time, room_id, model, operation, start_time, end_time, start_temp, end_temp, wind, fee_rate, fee)
                              values
                              (?, ?, ?, '0', ?, 0, ?, 0, ?, ?, 0)
            '''
            cursor.execute(addDetailSql, (detailCheckInTime2, int(i), detailModel2, detailStartTime2, detailStartTemp2, detailWind2, detailFeeRate2,))

            roomlist[i].dispatchfee = 0.0
            cursor.close()
            conn.commit()
            conn.close()

    while (len(servicelist)<host.numServe) and (len(waitlist) > 0): #服务队列不满，从等待队列里拿
        flag = True
        target = 0
        for i in waitlist.values():
            if flag :
                flag = False
                target = i
            else:
                if roomlist[i].waitclock < roomlist[target].waitclock:
                    target = i
        roomlist[target].isServing = 1
        del waitlist[target]
        servicelist[target] = target

        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        detailCheckInTime = roomlist[target].checkInTime
        detailModel = roomlist[target].mode
        detailStartTime = datetime.datetime.now()
        detailStartTemp = roomlist[target].currentTemp
        detailWind = roomlist[target].wind
        detailFeeRate = roomlist[target].fee_rate
        addDetailSql = '''insert into AirCondition_details
                          (check_in_time, room_id, model, operation, start_time, end_time, start_temp, end_temp, wind, fee_rate, fee)
                          values
                          (?, ?, ?, '0', ?, 0, ?, 0, ?, ?, 0)
        '''
        cursor.execute(addDetailSql, (detailCheckInTime, int(target), detailModel, detailStartTime, detailStartTemp, detailWind, detailFeeRate,))

        roomlist[target].dispatchfee = 0.0
        cursor.close()
        conn.commit()
        conn.close()