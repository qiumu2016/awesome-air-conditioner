from django.db import models


from django.db import models

#房客每一操作对应的参数
class Details(models.Model):
    id = models.AutoField(primary_key=True)
    check_in_time = models.DateTimeField()
    room_id = models.IntegerField()
    model = models.CharField(max_length=10) #制冷制热
    operation = models.CharField(max_length=15) #调温调风
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_temp = models.FloatField()
    end_temp = models.FloatField()
    wind = models.CharField(max_length=10) #风速
    fee_rate = models.FloatField()
    fee = models.FloatField()   #此次操作产生的费用

#房客从入住到退房的信息
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.IntegerField()
    switch = models.IntegerField()  #开关了多少次
    time = models.IntegerField() #入住时间
    fee = models.FloatField()
    schedule = models.IntegerField() #调度次数
    change_temp = models.IntegerField() #改变温度的次数
    change_wind = models.IntegerField() #改变风速的次数

