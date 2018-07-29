from flask import json ,render_template ,request ,redirect ,url_for

from monitor_cfg import *
import monitor_cfg
import requests
#flask_login  魔法模块,不知道怎么就工作了,暂时搞不明白怎么玩的

@login_manager.user_loader  # 使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态
def load_user(id):  # 这个id参数的值是在 login_user(user)中传入的 user 的 id 属性
    return User.query.get(int(id))





#监控首页,展示各种栏目,主体有图表
@app.route('/monitor', methods=['GET','POST'])
@login_required
def monitor():
    count = DeviceInfo.query.count()
    onl =DeviceInfo.query.filter_by(devicestat=True).count()
    offl =DeviceInfo.query.filter_by(devicestat=False).count()
    updatatime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    about = DeviceStat.query.order_by('-id').limit(7) #以数据库里的ID为基准的输出  -id 为倒叙
    aboutol =[]
    aboutoffl =[]
    for x in about :
        aboutol.append(int(x.ol))
        aboutoffl.append(int(x.offl))
    return render_template('index.html' ,title=ConfigInfo.query.first().title,footer = ConfigInfo.query.first().footer ,updatatime=updatatime , offl=offl,onl=onl, count=count,aboutol=aboutol,aboutoffl=aboutoffl)

#设备历史在线状态线图
@app.route('/detail/')
@login_required
def detail():
    return render_template('detail.html' ,title=ConfigInfo.query.first().title,footer = ConfigInfo.query.first().footer)


#监控设置页
@app.route('/config',methods=['GET','POST'])
@login_required
def config():
    if request.method == 'GET' :
        return render_template('config.html' ,title=ConfigInfo.query.first().title ,footer = ConfigInfo.query.first().footer )
    elif request.method == 'POST':
        if request.form['title'] != '' :
            config = ConfigInfo.query.first()
            config.title = request.form['title']
            db.session.add(config)
            db.session.commit()
        if request.form['footer'] != '' :
            config = ConfigInfo.query.first()
            config.footer = request.form['footer']
            db.session.add(config)
            db.session.commit()
        return redirect(url_for('config'))
        
        ##ConfigInfo.query.first().footer = request.form['footer']
        

#登陆页面
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET' :
        return render_template('login.html' ,title=ConfigInfo.query.first().title,footer = ConfigInfo.query.first().footer)
    

#登录验证页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST' :
        user = User.query.filter_by(username=request.form['account']).first()
        if user == None :
            return '用户不存在'
        elif user.password ==request.form['password'] :
            login_user(user)
            return redirect(url_for('monitor'))
        else:
            return '密码错误或者账户异常!'

@app.route('/test')
def test():
    username =current_user.username
    return  username

#API
@app.route('/api',methods=['GET','POST'])
def api():
    if request.method == 'GET' :
        page =  request.args.get('page')  #获取页数
        limit = request.args.get('limit') #获取每页行数
        a = int(page)*int(limit)          #分页上限数
        b = a-int(limit)                  #分页下限数
        ip_data = DeviceInfo.query.filter(DeviceInfo.id >=b,DeviceInfo.id <=a ).all()
        ip_datacount = DeviceInfo.query.count()
        ip_json = []
        n = 0
        for x in ip_data :
            ip_json.append(x.to_json())
        x= '{"code":0,"msg":"","count":%i,"data":%s} '%(ip_datacount,json.dumps(ip_json))
    return x

#设备历史在线状态线图
@app.route('/history/<ip>')
@login_required
def history(ip):
    #http://localhost:8086/query?epoch=ms&q=select value  from mydb..Host_Stat where ip=\'%s\'' %ip
    #select value from Host_Stat where ip='172.17.41.34' and time > now() -7d   查询7天内的数据
    #monitor_web内API拼接最终地址
    influx_geturl = '%s\'%s\'' %(monitor_cfg.influx_apigeturl,ip)
    influx_get = requests.get(influx_geturl)
    influx_get=json.loads(influx_get.text)
    datatime=[]
    datastat=[]
    for x in influx_get['results'][0]['series'][0]['values'] :
        datastat.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x[0]/1000)))
        datatime.append(x[1])
    try :
        return render_template('history.html',datatime=datatime,datastat=datastat,ip=ip ,title=ConfigInfo.query.first().title,footer = ConfigInfo.query.first().footer)
    except :
        #如遇异常,比如JSON获取不正确,或其他错误统一返回暂无数据,以后在添加一些其他异常返回
        return '<h1 align="center">目暂无数据!</h1>'

#退出登录
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '退出登录!'

if __name__ == '__main__':
    manager.run()
