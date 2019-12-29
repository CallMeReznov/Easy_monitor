from flask import Flask
from flask_script import Manager
from flask import render_template
from flask import json
from flask import request
import monitor_cfg
import requests

app =Flask(__name__)
manager = Manager(app)

#游览器获取首页页面信息
@app.route('/', methods=['GET'])
def login_form():
    return render_template('index.html',title = monitor_cfg.config_webtitle,info = monitor_cfg.config_webinfo)


#获取对比/ POST过来的信息成功后载入IP.JSON并传送到monitor模版上
@app.route('/monitor', methods=['POST'])
def login_signin():
    if request.form['username']==monitor_cfg.config_user and request.form['password']==monitor_cfg.config_passwd :
        with open('static/ip.json','r') as f :
            host_json = json.load(f)
        return render_template("monitor.html",title = monitor_cfg.config_webtitle,data = json.dumps(host_json,ensure_ascii=False) )
    else:
        return '<h1 align="center">账号或密码错误!</h1>'


#点击详细链接后传送IP查询influxd API并返回数据进detail模版打入Highstock模版内
@app.route('/detail/<ip>')
def monitor_detail(ip):
    #influx_geturl ='http://localhost:8086/query?epoch=ms&q=select value  from mydb..Host_Stat where ip=\'%s\'' %ip
    #monitor_web内API拼接最终地址
    influx_geturl = '%s\'%s\'' %(monitor_cfg.influx_apigeturl,ip)
    influx_get = requests.get(influx_geturl)
    influx_get=json.loads(influx_get.text)
    try :
        return render_template('detail.html',title = monitor_cfg.config_webtitle,data=influx_get['results'][0]['series'][0]['values'],ip=ip)
    except :
        #如遇异常,比如JSON获取不正确,或其他错误统一返回暂无数据,以后在添加一些其他异常返回
        return '<h1 align="center">目暂无数据!</h1>'


if __name__ == '__main__':
    manager.run()
