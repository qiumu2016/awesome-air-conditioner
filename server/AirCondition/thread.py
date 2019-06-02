import threading
import time
import datetime
from . import search
import sqlite3


dbpath = 'db [2]'

def tempcalc(smode,swind): #根据冷热风速计算变化速率
    temp = 0.0
    if swind == 'low':
        temp = 0.5
    elif swind == 'mid':
        temp = 1.0
    else:
        temp = 1.5
    if smode == 'cold':
        temp = - temp
    return temp

class myThread(threading.Thread):
    def run(self):
        while 1:
            time.sleep(60)
            for i in search.servicelist: #正在空调服务的房间空调变化
                for j in search.serviceobjlist:
                    obj = search.servicelist[j.dispatchid]
                    obj.fee += obj.fee_rate
                    search.roomlist[obj.roomid].currentTemp += tempcalc(obj.mode,obj.wind)
                    if (obj.mode == 'cold' and search.roomlist[obj.roomid].currentTemp < obj.target_temp) or (obj.mode == 'hot' and search.roomlist[obj.roomid].currentTemp > obj.target_temp) : #服务结束
                        roomid = obj.roomid
                        search.roomlist[roomid].currentTemp = obj.target_temp
                        search.roomlist[roomid].isServing = 0
                        serviceid = search.roomlist[roomid].serviceid
                        del search.servicelist[obj.id]
                        del search.serviceobjlist[serviceid]

                        t2 = datetime.datetime.now()

                        conn = sqlite3.connect(dbpath)
                        cursor = conn.cursor()
                        queryDetailSql = '''select MAX(id)
                                            from AirCondition_details
                                            where room_id = ?
                        '''
                        cursor.execute(queryDetailSql,roomid)
                        updateIdList = cursor.fetchone()
                        updateIdStr = "".join(updateIdList)
                        updateId = int(updateIdStr)
                        updateDetailSql = '''update AirCondition_details
                                             set end_time = ?, end_temp = ?, fee = ?
                                             where id = ?
                        '''
                        cursor.execute(updateDetailSql, (t2, search.roomlist[obj.roomid].currentTemp, obj.fee, updateId))

                        cursor.close()
                        conn.commit()
                        conn.close()


            for i in search.waitlist : #等待队列的等待时间减一
                i.waittime -= 1
                if i.waittime == 0: #已经到时，强行入队
                    flag = True 
                    target = 0
                    for j in search.serviceobjlist :
                        if flag :
                            flag = False
                            target = j
                        else:
                            if target.clock > j.clock :
                                target = j
                    del search.serviceobjlist[target.id]
                    obj2 = search.servicelist[target.dispatchid]
                    del search.servicelist[obj2]
                    search.waitlist[obj2.id] = obj2
                    obj2.waitclock = time.time()
                    obj2.waittime = 2
                    search.roomlist[target.roomid].isServing = 0
                    del search.waitlist[i.id]
                    search.servicelist[i.id] = i
                    serviceobject = search.serviceobj(i.roomid) #新建一个服务对象
                    i.serviceid = serviceobject.id
                    serviceobject.dispatchid = i.id
                    search.roomlist[i.roomid].isServing = 1
                    serviceobject.status = 1
                    search.serviceobjlist[serviceobject.id] = serviceobject
            while (len(search.servicelist)<search.host.numServe) and (len(search.waitlist) > 0): #服务队列不满，从等待队列里拿
                obj = 0
                flag = True
                for i in search.waitlist:
                    if flag :
                        flag = False
                        obj = i
                    else:
                        if i.waitclock < obj.waitclock:
                            obj = i
                roomid = obj.roomid
                serviceobject = search.serviceobj(roomid) #新建一个服务对象
                obj.serviceid = serviceobject.id
                serviceobject.dispatchid = obj.id
                search.roomlist[roomid].isServing = 1
                serviceobject.status = 1
                search.serviceobjlist[serviceobject.id] = serviceobject
                del search.waitlist[obj]
                search.servicelist[obj.id] = obj
thread1 = myThread(1, "Thread-1", 1)

thread1.start()