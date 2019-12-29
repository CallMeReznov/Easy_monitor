from flask import Flask
from flask_script import Manager
from flask import render_template
import json
#载入app设置
#import monitor_config





app = Flask(__name__)
manager = Manager(app)
#app.config.from_objec(monitor_config)
@app.route('/')
def index():
    return 'Hello World'

@app.route('/monitor')
def monitor():
    #载入本地JSON数据
    with open('static/data.json','r') as f:
        host_json = json.load(f)
    return render_template("index.html",data = json.dumps(host_json,ensure_ascii=False) )

if __name__ == '__main__':
   manager.run()
