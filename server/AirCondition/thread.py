import threading
import time
import datetime
from . import search
import sqlite3
import os

dbpath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db.sqlite3')

class myThread(threading.Thread):
    def run(self):
        while 1:
            time.sleep(1)
            for i in search.servicelist.values(): #正在空调服务的房间空调变化
                for j in search.serviceobjlist.values():
                    obj = search.servicelist[j.dispatchid]
                    temp = obj.fee_rate / 60.0
                    obj.fee += temp
                    search.roomlist[obj.roomid].fee += temp
                    if obj.mode == 'cold' :
                        temp = -temp
                    search.roomlist[obj.roomid].currentTemp += temp
                    if (obj.mode == 'hot' and search.roomlist[obj.roomid].currentTemp >= obj.target_temp) or (obj.mode == 'cold' and search.roomlist[obj.roomid].currentTemp <= obj.target_temp) : #服务结束
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
                        cursor.execute(queryDetailSql,(int(roomid),))
                        updateIdList = cursor.fetchone()
                        updateIdStr = str(updateIdList)[1:-2]
                        updateId = int(updateIdStr)
                        updateDetailSql = '''update AirCondition_details
                                             set end_time = ?, end_temp = ?, fee = ?
                                             where id = ?
                        '''
                        cursor.execute(updateDetailSql, ((t2, search.roomlist[obj.roomid].currentTemp, obj.fee, updateId),))

                        cursor.close()
                        conn.commit()
                        conn.close()


            for i in search.waitlist.values() : #等待队列的等待时间减一
                i.waittime -= 1
                if i.waittime == 0: #已经到时，强行入队
                    flag = True 
                    target = 0
                    for j in search.serviceobjlist.values() :
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
                for i in search.waitlist.values():
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