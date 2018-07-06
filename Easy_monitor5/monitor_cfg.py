import msvcrt
#检测键盘输入
def kb_hitchk():
    Kb_hit =msvcrt.kbhit()
    if Kb_hit :
        Kb_return = ord(msvcrt.getch())
    else :
        Kb_return = 0
    return Kb_return

#前端显示名称
config_webtitle = ''
#前端底部页面信息
config_webinfo = ''
#需监控前端设备地址列表文件,csv后缀,格式 "设备名称,设备地址,设备端口"
config_ipfile = './static/ip.csv'
#超时时间,建议默认1秒
config_timeout = 1
#生成的JSON文件路径
config_jsflie = './static/ip.json'
#用户名,密码
config_user='test'
config_passwd='test'
#influxdb HTTPAPI地址
influx_apigeturl ='http://localhost:8086/query?epoch=ms&q=select value  from mydb..Host_Stat where ip='
influx_apiposturl='http://localhost:8086/write?db=mydb'