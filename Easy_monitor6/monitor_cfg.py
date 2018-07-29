import os ,msvcrt ,time
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager ,Server
from flask_login import LoginManager, current_user, login_user, login_required ,UserMixin ,login_user ,logout_user

app = Flask(__name__)
manager = Manager(app)
#DEBUG模式
#manager.add_command("runserver", Server(use_debugger=True))
app.secret_key = 'Sqsdsffqrhgh.,/1#$%^&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./monitor.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'
#login_manager.login_message = '请登录!'

#类名使用驼峰命名风格
#变量小写,常量大写
#用户表,账号密码
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

#设备信息表,设备地址,名称,类型,端口,状态
class DeviceInfo(db.Model):
    __tablename__ = 'deviceinfo'
    id = db.Column(db.Integer,primary_key=True) 
    deviceip = db.Column(db.String(64),unique=True)#设备IP地址,不允许重复
    devicename = db.Column(db.String(64)) #设备名
    devicearea = db.Column(db.String(64)) #设备区域
    devicetype = db.Column(db.String(64)) #设备类型
    deviceport = db.Column(db.Integer) #设备端口
    devicestat = db.Column(db.Boolean) #设备状态,默认不在线
    devicerem = db.Column(db.String(128))
    
    def __init__(self,deviceip,devicename,devicetype,deviceport,devicestat,devicearea):
        self.deviceip = deviceip
        self.devicename = devicename
        self.devicetype = devicetype
        self.deviceport = deviceport
        self.devicestat = devicestat
        self.devicearea = devicearea

    def to_json(self):
        return{
            'id':self.id,
            'title':self.devicename,
            'ip':self.deviceip,
            'port':self.deviceport,
            'type':self.devicetype,
            'stat':self.devicestat,
            'area':self.devicearea
        }

    def __repr__(self):
        return '<Devicename %r>' % self.devicename

#程序信息设置
class ConfigInfo(db.Model):
    __tablename__ = 'configinfo'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(128)) #首页标题
    footer =  db.Column(db.String(128)) #首页页脚

    def __init__(self,title,footer):
        self.title = title
        self.footer = footer

#记录每日点位状态
class DeviceStat(db.Model):
    __tablename__ = 'devicestat'
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(12)) #日期
    ol = db.Column(db.String(8)) #在线数量
    offl =  db.Column(db.String(8)) #离线数量

    def __init__(self,date,ol,offl):
        self.date = date
        self.ol = ol
        self.offl = offl


#influxdb HTTPAPI地址
#influx_apigeturl ='http://localhost:8086/query?epoch=ms&q=select value  from mydb..Host_Stat where ip='
influx_apigeturl ='http://localhost:8086/query?epoch=ms&q=select value from mydb..Host_Stat where time > now() -7d and ip='
influx_apiposturl='http://localhost:8086/write?db=mydb'

#设备测试超时时间,建议默认1秒
config_timeout = 1