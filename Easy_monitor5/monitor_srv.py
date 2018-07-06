import time
import socket
import json
import monitor_cfg
import requests

while True:
    #开始循环检测host_iplist内所有地址
    #循环前初始化
    json_payload = []
    host_iplist = []
    print('载入地址列表文件....')
    #载入需要监控的IP地址列表
    for host_line in open(monitor_cfg.config_ipfile,'r'):
        host_iplist.append(host_line.strip('\n'))
    host_len = int(len(host_iplist))
    print('当前列表内共有%s条信息'%host_len)
    print('载入地址列表文件完毕')
    print('开始循环检测地址列表文件内地址....')
    print('按Esc键退出程序....')
    #分隔当前循环中的数据信息 名称,IP,端口
    
    for host_row in host_iplist :
        #检测键盘输入,输入esc退出
        Host_kbchk = monitor_cfg.kb_hitchk()
        if Host_kbchk == 27 :
            exit()
        host_name = host_row.split(',')[0]
        host_ip = host_row.split(',')[1]
        host_port = host_row.split(',')[2]

        try:
            #测试目标IP端口是否有回应  超时时间为monitor_cfg.config_timeout
            #为了防止过快访问默认延迟1秒
            host_iptest = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            host_iptest.settimeout(monitor_cfg.config_timeout)
            host_iptest.connect((host_ip,int(host_port)))
            host_iptest.close()
            host_stats = 1
        except socket.timeout :
            host_stats = 0
            host_iptest.close
            
        host_timestamp = time.asctime(time.localtime(time.time()))
        host_info = {
            'hostname': host_name,
            'ip': host_ip,
            'timestamp': host_timestamp,
            'stats': host_stats,
            } 
        print("当前测试信息:")
        print("前端设备名称 ",host_name)
        print("前端设备地址 ",host_ip)
        print("设备测试端口 ",host_port)
        print("前端设备状态 ",host_stats)        
        json_payload.append(host_info)
        #拼接字符串提交influx API     因为可能influx自带的时间戳不是太正常加上本地时间*1000是毫秒符合influx的格式
        influx_postdata = '%s,host=%s,ip=%s value=%s %s' %('Host_Stat',host_name,host_ip,host_stats ,int(time.time()*1000000000))
        #influx_postdata = '%s,host=%s,ip=%s value=%s ' %('Host_Stat',host_name,host_ip,host_stats)
        print(influx_postdata)
        #还没增加错误判断 连不上influxAPI会报错
        requests.post(monitor_cfg.influx_apiposturl, data=influx_postdata.encode('utf-8'))
        
    #内循环完毕写入monitor首页JSON文件
    with open(monitor_cfg.config_jsflie,'w') as f :
        json.dump(json_payload,f)
        print('写入成功')
