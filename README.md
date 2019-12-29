# Easy_monitor


## 介绍
把之前Flask写的后台转到了Django上,几乎没写代码就轻松移植了过来,全部是用的是DJANGO-ADMIN自带的功能.  
也把Ser部分重写了,influx部分直接调轮子.劲量减少代码.





#### 开发环境
* Python 3.6.7
* DBUtils==1.3
* Django==3.0
* django-admin-view-permission==1.9
* django-adminlte-ui==1.4.0
* django-treebeard==4.3
* influxdb==5.2.3


#### 使用说明

先生成数据库    `.\manage.py migrate`  
在新建一个管理账户  `.\manage.py  createsuperuser`  
最后启动Django `.\manage.py runserver`    
登陆后台[localhost](http://localhost:8000),最少添加一个设备列表保存  
配置好influxdb服务的相关配置,需要的配置写在Monitor_Ser的头几行里  
启动Monitor服务`Monitor_Ser.py`     

 Old_version 弃用   