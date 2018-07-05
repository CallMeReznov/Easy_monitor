# Easy_monitor

--------------
#### 干嘛用的？
早期这个项目本身是因为公司不存在最简易监控摄像头在线情况的业务,使用ZABBIX又太过于麻烦所以就想顺便学习一下python,json,opentsdb的知识,并没有把它写成一个真正的监控系统,不过随着版本的更新与学习的进一步,我对于这个项目的最终目标是可以做到MVC架构的时间序列监控程序(可能还会加上心跳?)


#### 开发环境
* visual studio code
* python3<br>
* opentsdb<br>
* hbase1.4.3<br>
* opentsdb2.3.0
<br>**需要注意**<br>如果想直接不修改脚本并支持中文需要对opentsdb进行源码修改编译安装，修改源码编码为UTF-8
opentsdb的官方说至少要到3.0才会想办法支持UTF-8
* grafana5.0.4<br>
* [bcgrid](https://github.com/bigq517/bcgrid/)
* msvcrt,time,socket,json,flask python模块
#### 项目结构
* Easy_monitor1<br>
利用OPENTSDB存储数据,grafana展示,python处理数据的方式,oepntsdb部署起来过于麻烦,已经抛弃
1. opentsdb.py **主文件**
2. ip.csv  **需要监控的IP列表文件**
3. err.log **错误信息日志**
4. config.ini **配置文件，主要脚本的说明信息都在里面了**
* Easy_monitor2<br>
引入了[bcgrid](https://github.com/bigq517/bcgrid/)利用专用HTTP服务器托管静态HTML页面载入表格插件显示数据(不过因为不会js jq之类的技术无法动态载入所以数据无法排序分页)
1. monitor.py **主文件**
2. ip.csv  **需要监控的IP列表文件**
3. config.ini **配置文件，主要脚本的说明信息都在里面了**
4. html/ **静态页面**
* Easy_monitor3<br>
使用flask框架把JSON数据打入页面,利用本身表格插件的功能去除了之前无法排序分页的BUG,且使用FLASK本身自带的HTTP服务可以直接使用pyinstaller编译部署到服务器上运行,简单方便好处多多(无法适应大批量)
1. monitor_server.py **监控程序主文件**
2. ip.csv  **需要监控的IP列表文件**
3. config.ini **配置文件，主要脚本的说明信息都在里面了**
4. monitor/monitor_web.py **前端动态页面**
5. monitor/templates monitor/templates **前端动态页面资源页**
6. monitor/templates/static/data.json **生成的JSON文件由动态载入**
* Easy_monitor4<br>
整体重构了结构与代码以便下个版本引入数据库和真正的MVC框架<br>
添加了简单的登陆验证GET POST,引入了bootstrap框架,FLASK模板继承等新知识<br>
现在算是一个比较简单易懂的版本了,拿到手修改cfg就能跑


#### 作者列表

**我**



#### 更新链接

**暂时没有**



#### 历史版本
* Easy_monitor1
* Easy_monitor2
* Easy_monitor3
* Easy_monitor4

#### 联系方式

**无可奉告**