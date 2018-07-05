from flask import Flask
from flask_script import Manager
from flask import render_template
from flask import json
from flask import request
import monitor_cfg


app =Flask(__name__)
manager = Manager(app)

#游览器获取首页页面信息
@app.route('/', methods=['GET'])
def login_form():
    return render_template('index.html',title = monitor_cfg.config_webtitle,info = monitor_cfg.config_webinfo)

@app.route('/monitor', methods=['POST'])
def login_signin():
    if request.form['username']==monitor_cfg.config_user and request.form['password']==monitor_cfg.config_passwd :
        with open('static/ip.json','r') as f :
            host_json = json.load(f)
        return render_template("monitor.html",title = monitor_cfg.config_webtitle,data = json.dumps(host_json,ensure_ascii=False) )
    else:
        return '<h1 align="center">账号或密码错误!</h1>'

if __name__ == '__main__':
    manager.run()
