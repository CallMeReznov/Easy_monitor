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
#提交JSON
def Js_Send(json):
    Js_return = requests.post(Host_Config.get('Host_config','Host_Url'), json=json)
    return Js_return.text  
#检测键盘输入
def Kb_hitchk():
    Kb_hit =msvcrt.kbhit()
    if Kb_hit :
        Kb_return = ord(msvcrt.getch())
    else :
        Kb_return = 0
    return Kb_return
#载入csv
print('载入地址列表文件')
for line in open(Host_Config.get('Host_config','Host_File'),'r'):   
    Host_Iplist.append(line.strip('\n'))
while True:
    print('开始循环检测地址列表文件内地址....')
    print('按Esc键退出程序....')
    for Host_Row in Host_Iplist:
        Host_kbchk = Kb_hitchk()
        if Host_kbchk == 27 :
            break
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

        Host_Timestamp=time.time()
        payload = {
            'metric': Host_Config.get('Host_config','Host_Metric'),
            'timestamp': Host_Timestamp,
            'value': Host_stats,
            'tags': {
                'host': Host_name,
                'ip': Host_ip
            }
        }
        print("当前测试信息:")
        print("前端设备名称 ",Host_name)
        print("前端设备地址 ",Host_ip)
        print("设备测试端口 ",Host_port)
        print("前端设备状态 ",Host_stats)
        #print(send_json(payload))
        Host_Result=json.loads(Js_Send(payload))
        if Host_Result['success'] == 1:
            print('提交成功')
            #print(Host_Result)
            print('----------------------------------------------')
        else :
            print('提交失败,请查询脚本日志!')
            #print(Host_Result)
            Host_Err = open(Host_Config.get('Host_config','Host_Errlog'), 'a')
            Host_Err.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            Host_Err.write(':')
            Host_Err.write(str(Host_Result))
            Host_Err.write('\n')
            Host_Err.close()
            print('----------------------------------------------')
    if Host_kbchk == 27 :
        print('程序退出....')
        break