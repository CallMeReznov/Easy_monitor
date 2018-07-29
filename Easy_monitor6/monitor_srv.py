from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import socket ,time ,requests ,os ,monitor_cfg
from monitor_cfg import User ,db ,DeviceInfo ,DeviceStat
import json

#TODO :自动创建数据库后没有任何数据,需要写个判断否则会报错
#if os.path.exists('monitor.db') == False :
#    print ('设备信息库不存在,自动创建!请添加基础数据!')
#    db.create_all()

#打开数据库载入所有记录,装入循环
#循环测试每一个IP,把结果写入数据库,并提交给influxAPI
while True :
    #从ORM里提取表内所有数据
    ip_list = DeviceInfo.query.all()
    #print(ip_list)
    #计算数据条目数作为循环上限值
    ip_listcount = DeviceInfo.query.count()
    #累加器清0开始循环测试
    n = 0 
    while n < ip_listcount :
        try:
            #测试目标IP端口是否有回应  超时时间为monitor_cfg.config_timeout
            #每一次连接测试都提交到数据库,以后看看循环完毕后一次性提交会不会比较好
            host_iptest = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            host_iptest.settimeout(monitor_cfg.config_timeout)
            host_iptest.connect((ip_list[n].deviceip,ip_list[n].deviceport))
            host_iptest.close()
            host_stats = 1
            ip_list[n].devicestat = host_stats
            #时间戳未添加
            db.session.commit()
        except socket.timeout :
            host_stats = 0
            host_iptest.close()
            ip_list[n].devicestat = host_stats
            #时间戳未添加
            db.session.commit()
        #打印当前点位信息
        print('设备列表总第%s条数据' %n)
        print('设备IP:%s' %ip_list[n].deviceip)
        print('设备端口:%s' %ip_list[n].deviceport)
        print('设备状态:%s' %ip_list[n].devicestat)
        print('----------------------------------------------------------------------')
        #拼接字符串提交influx API     因为可能influx自带的时间戳不是太正常加上本地时间*1000是毫秒符合influx的格式
        influx_postdata = '%s,host=%s,ip=%s value=%s %s' %('Host_Stat',ip_list[n].devicename,ip_list[n].deviceip,host_stats ,int(time.time()*1000000000))
        #print(influx_postdata)
        #TODO :还没增加错误处理 连不上influxAPI会报错
        requests.post(monitor_cfg.influx_apiposturl, data=influx_postdata.encode('utf-8'))
        n= n + 1
        print(time.strftime("%H:%M", time.localtime()))
        #设定在每天的一个时间生成一次统计信息
        if time.strftime("%H:%M", time.localtime()) == "08:45" :
            ds = DeviceStat(date=time.strftime("%Y-%m-%d", time.localtime()),ol=DeviceInfo.query.filter_by(devicestat=True).count(),offl=DeviceInfo.query.filter_by(devicestat=False).count())
            db.session.add(ds)
            db.session.commit()
            print('生成今日统计信息')
            time.sleep(60)