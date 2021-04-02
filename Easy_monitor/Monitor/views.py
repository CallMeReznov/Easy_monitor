from django.shortcuts import render
from django.http import HttpResponse
from urllib3.request import RequestMethods
from .models import DeviceInfo ,DeviceCountHistory
from django.template import loader
from django.contrib.auth.decorators import login_required
from influxdb import InfluxDBClient
import requests ,json, urllib3
#urllib3.util.url.FRAGMENT_CHARS|={"&"}
infhost ='localhost'
infport ='8086'
infuser ='myadmin'
infpswd = 'test!2345'
infdb = 'mydb'

#摄像头账号密码
camerauser = 'admin'
camerapswd = '123456'

#MediaServer地址
mdserver = '127.0.0.1'

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


@login_required(login_url='/admin')
def devicestatpreview(request,deviceip):
    context = {'host': deviceip}
    return render(request, 'Monitor/preview.html', context)

#如果为了安全可以在mdserver的webhook地址上加个参数token之类的验证,接口在验证一下就好了,本身可以只限制本地提交
def notfound(request):
    streamid = json.loads(request.body)
    streamip = DeviceInfo.objects.get(deviceid=streamid['stream']).deviceip
    if DeviceInfo.objects.get(deviceid=streamid['stream']).devicetype == '海康' :
        print('海康设备')
        streamurl = 'rtsp://%s:%s@%s/cam/realmonitor?channel=1?6subtype=0' %(camerauser,camerapswd,streamip)
    elif DeviceInfo.objects.get(deviceid=streamid['stream']).devicetype == '大华' :
        print('大华设备')
        streamurl = 'rtsp://%s:%s@%s:554/cam/realmonitor?channel=1?subtype=0' %(camerauser,camerapswd,streamip)
    streamurldst = 'rtmp://%s/live/%s' %(mdserver,streamid['stream'])
    requests.post(r"http://%s/index/api/addFFmpegSource?src_url=%s&dst_url=%s&timeout_ms=10000&enable_hls=0&enable_mp4=0" %(mdserver,streamurl,streamurldst))
    return HttpResponse('200')


def notread(request):
    streamid = json.loads(request.body)
    print('无人观看')
    requests.post('http://'+mdserver+'/index/api/close_streams',data={'schema':'rtsp','vhost':'__defaultVhost__','app':'live','stream':streamid['stream'],'force':1})
    return HttpResponse('200')
