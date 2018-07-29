# Easy_monitor6

--------------
#### 应用简介
此版本为Easy_monitor的第六个版本,经过之前的各种学习和尝试,现在这个版本趋向于稳定,今后也不会在此基础上进行较大的更新了了<br>
此版本按照我学习到的方法,在后端引入了ORM模型,把之前CSV数据存储到了SQLITE数据库内,前端尝试完全使用了整套独立的UI框架<br>
虽然代码很乱,也没有良好的命名习惯,但总算是迈了第一步出去了.<br><br>
**注意:**<br>
设备管理与账户管理这两个功能我暂时还没做.<br>
因为使用了隐式引用导致无法使用pyinstall软件编译成EXE

#### 开发环境
* visual studio code
* python3<br>
* Influxdb<br>
* Layui<br>
* [Vip-Admin UI模版](http://vip-admin.com/product/1.html)
#### 项目结构
1. monitor_cfg.py **模型对象以及其他一些设置**
2. monitor_srv.py  **监控后端程序,单线程循环检测端口,并在指定时间内生成每日的概况数据(写的很懒)**
3. monitor_web.py **监控WEB主程序**
4. templates **模版文件夹**
5. static **静态文件文件夹**
6. monitor.db **监控数据库**
7. Influxdb **Influx教程网上到处都是,搭建起来后在CFG里修改一下API即可**

#### 使用方法
第一次使用请进入python命令行下手动生成数据库,并且按照数据库格式手动添加数据<br>
>>> from monitor_cfg import db
>>> db.create_all()