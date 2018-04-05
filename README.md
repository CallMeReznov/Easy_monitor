﻿# Easy_monitor

---
## 干嘛用的？
其实就是个很简单的端口测试脚本，使用opentsdb后在grafana上展示测试目标的当前以及历史状态
主要是为了简单的监控前端网络摄像头的存活状态

---
## 开发环境\<br>
测试开发的环境基于\<br>
python3\<br>
opentsdb\<br>
hbase1.4.3\<br>
opentsdb2.3.0\<br>
grafana5.0.4\<br>
**需要注意**的一点就是如果想直接不修改脚本并支持中文需要对opentsdb进行源码修改编译安装，修改源码编码为UTF-8
opentsdb的官方说至少要到3.0才会想办法支持UTF-8

---
##项目结构\<br>
opentsdb.py **主文件**\<br>
ip.csv  **需要监控的IP列表文件**\<br>
err.log **错误信息日志**\<br>
config.ini **配置文件，主要脚本的说明信息都在里面了**\<br>

---
##作者列表\<br>
我\<br>

---
##更新链接
暂时没有\<br>

---
##历史版本\<br>
还不存在\<br>

---
##联系方式\<br>
无可奉告\<br>