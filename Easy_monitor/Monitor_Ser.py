from influxdb import InfluxDBClient
import socket ,sqlite3 ,time ,threading 
from DBUtils.PersistentDB import PersistentDB

###################################
#判断设备是否在线的超时时间
time_out = 2
#数据库名(默认SQLITE)
dbname = 'db.sqlite3'
#influxdb数据库相关配置信息
infhost ='localhost'
infport ='8086'
infuser ='myadmin'
infpswd = 'test!2345'
infdb = 'mydb'

#二次封装SQLITE3,并且引入连接池和锁,否则会因为占用的问题报错.
class NewLite():
    def __init__(self,dbname):
        self.db = PersistentDB(sqlite3,maxusage=None,database=dbname,closeable=False)
        self.con = self.db.connection()
        self.cur = self.con.cursor()


    def select(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def execsql(self,sql,param=None):
        if param is None :
            self.cur.execute(sql)
        else :
            self.cur.execute(sql,param)
        self.con.commit()



infclient =InfluxDBClient(infhost,infport,infuser,infpswd,infdb)

lock =threading.Lock()
def dailytask():
    conloop = NewLite(dbname)
    while True :
        try :
            lock.acquire()
            dailycount =conloop.select('select count(deviceip)  from Monitor_deviceinfo')
            dailyonline =conloop.select('select count(deviceip)  from Monitor_deviceinfo  where devicestat= 1')
            dailyoffline = conloop.select('select count(deviceip)  from Monitor_deviceinfo  where devicestat= 0')
            conloop.execsql('insert into Monitor_devicecounthistory(devicecount,deviceonline,deviceoffline,date) values (?,?,?,datetime("now","+8 hour"))',(dailycount[0][0],dailyonline[0][0],dailyoffline[0][0]))
        except  :
            print("线程内任务执行错误")
        finally :
            print('每日统计结束,等待24小时重新执行')
            time.sleep(86400)
            lock.release()

#第一次尝试使用线程,太好用了!
timetask = threading.Thread(target=dailytask)
timetask.start()

con =NewLite(dbname)
    #获取/更新列表后再次进入循环
while True :
    #循环开始
    print('更新IP列表')
    ip_list = con.select('select deviceip,deviceport,devicename from Monitor_deviceinfo')
    for x in ip_list :
        ip = str(x[0])
        port = int(x[1])
        name = str(x[2])
        print(ip)
        host_iptest = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_iptest.settimeout(time_out)
        try:
            host_iptest.connect((ip,port))
            ip_stat = 1
        except socket.timeout :
            ip_stat = 0
        finally :
            host_iptest.close()
            #更新数据库的设备状态
            con.execsql('update Monitor_deviceinfo set devicestat=? ,deviceadt=datetime("now","+8 hour") where deviceip=?',(ip_stat,ip))
            #在INFLUXDB里插入当前状态,拼个json进去
            #实际上这个模块还是用requests实现的.
            infjson = [
                {
                    "measurement": "host_history_stat",
                    "tags": {
                        "host": ip
                        },
                        #"time":"time",
                        "fields": {
                            "status": ip_stat,
                            },
                            }]
            #无法连接Influxdb
            try :
                infclient.write_points(infjson)
            except :
                print('*'*25)
                print('Influxdb连接错误,未开启?')
                print('*'*25)

        continue