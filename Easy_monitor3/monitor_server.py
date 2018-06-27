import requests
import time
import socket
import json
import configparser
import msvcrt
#载入配置文件
Host_Config=configparser.ConfigParser()
Host_Config.read('config.ini')

Host_Iplist=[]
#载入csv
print('载入地址列表文件')
for line in open(Host_Config.get('Host_config','Host_File'),'r'):   
    Host_Iplist.append(line.strip('\n'))
Json_len=int(len(Host_Iplist))
while True:
    payload1=[]
    print('开始循环检测地址列表文件内地址....')
    print('按Esc键退出程序....')
    for Host_Row in Host_Iplist:
        Host_name=Host_Row.split(',')[0]
        Host_ip=Host_Row.split(',')[1]
        Host_port=Host_Row.split(',')[2]
        try:
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #测试超时时间单位秒
            sk.settimeout(int(Host_Config.get('Host_config','Host_Timeout')))
            sk.connect((Host_ip,int(Host_port)))
            sk.close()
            Host_stats=1
            time.sleep(1)
        except socket.timeout :
            #打印错误类型
            #print(e.__class__)
            Host_stats = 0
            #print(x)
            sk.close()
            time.sleep(1)

        Host_Timestamp=time.asctime( time.localtime(time.time()) )
        payload = {
            #'metric': Host_Config.get('Host_config','Host_Metric'),
            'hostname': Host_name,
            'ip': Host_ip,
            'timestamp': Host_Timestamp,
            'stats': Host_stats,
            }
        print("当前测试信息:")
        print("前端设备名称 ",Host_name)
        print("前端设备地址 ",Host_ip)
        print("设备测试端口 ",Host_port)
        print("前端设备状态 ",Host_stats)
        #print(send_json(payload))
        payload1.append(payload)
    #写入文件
    with open('./monitor/static/data.json', 'w') as f:
        json.dump(payload1,f)
