from django.shortcuts import render
from django.http import HttpResponse
from .models import DeviceInfo ,DeviceCountHistory
from django.template import loader
from django.contrib.auth.decorators import login_required
from influxdb import InfluxDBClient
infhost ='localhost'
infport ='8086'
infuser ='myadmin'
infpswd = 'test!2345'
infdb = 'mydb'

infclient =InfluxDBClient(infhost,infport,infuser,infpswd,infdb)
# Create your views here.

@login_required(login_url='/admin') #只允许在后台登陆的时候访问,如没登陆就转到/admin页面进行登陆
def index(request):

    lasttime= DeviceInfo.objects.order_by('deviceadt').last() 
    alldevice = DeviceInfo.objects.all().count()
    offdevice = DeviceInfo.objects.filter(devicestat=0).count()
    oldevice = DeviceInfo.objects.filter(devicestat=1).count()
    #最后7条记录,使用切片 最近7天的在线数据
    weekstat =DeviceCountHistory.objects.all()[:7]
    weekonline =[]
    weekoffline =[]
    for y in weekstat :
        weekonline.append(y.deviceonline)
        weekoffline.append(y.deviceoffline)


    
    context = {'lasttime':lasttime.deviceadt,'count':alldevice,'ol':oldevice,'offl':offdevice,'wol':weekonline,'woffl':weekoffline}

    return render(request, 'Monitor/index.html', context)

@login_required(login_url='/admin')
def devicestathistory(request,deviceip):
    #通过IP查询influxdb数据库内最后1000条记录
    infsql = "SELECT * from host_history_stat where host='%s' order by time desc  limit 1000" %deviceip
    rs= infclient.query(infsql)
    stat_points = list(rs.get_points(measurement='host_history_stat'))
    #生成列表传入前端echarts
    hoststat = []
    hosttime = []
    for x in stat_points :
        hoststat.append(x['status'])
        hosttime.append(x['time'])
    context = {'host': deviceip,'time':hosttime,'status':hoststat}
    return render(request, 'Monitor/history.html', context)
