import threading
import time
from . import search

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
            for i in search.servicelist:
                for j in search.serviceobjlist:
                    obj = search.servicelist[j.dispatchid]
                    obj.fee += obj.fee_rate
                    search.roomlist[obj.roomid].currentTemp += tempcalc(obj.mode,obj.wind)
                    if (obj.mode == 'cold' and search.roomlist[obj.roomid].currentTemp < obj.target_temp) or (obj.mode == 'hot' and search.roomlist[obj.roomid].currentTemp > obj.target_temp) :
                        search.roomlist[obj.roomid].currentTemp = obj.target_temp
                        
            for i in search.waitlist :
                i.waittime -= 1
                if i.waittime == 0:
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

thread1 = myThread(1, "Thread-1", 1)

thread1.start()