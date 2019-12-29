from django.db import models
from django.utils.html import format_html
# Create your models here.

class DeviceInfo(models.Model):
    #DeviceInfo.objects.all返回STR内容
    def __str__(self):
        return self.devicename

    class Meta:
        verbose_name = '设备列表'    # 表名改成中文名
        verbose_name_plural = verbose_name

    deviceid =models.IntegerField(primary_key=True,verbose_name="设备序号")  
    deviceip =models.CharField(max_length=64,unique=True,verbose_name="设备地址") #设备IP地址,不能重复
    devicename =models.CharField(max_length=64,verbose_name="设备名称")  #设备名
    devicearea =models.CharField(max_length=64,verbose_name="设备区域")  #设备区域
    devicetype =models.CharField(max_length=64,verbose_name="设备类型")  #设备类型
    deviceport =models.IntegerField(verbose_name="设备端口")  #设备端口
    devicestat =models.BooleanField(verbose_name="设备状态")   #设备状态
    devicerem =models.CharField(max_length=256,null=True,blank=True,verbose_name="备注")   #设备
    deviceadt =models.DateTimeField(auto_now_add=True,null=True,verbose_name="设备添加时间")
    

    def history(self):
        self.verbose_name= "历史"
        return  format_html('<a href="/monitor/history/%s">历史记录</a>' %(self.deviceip))



class DeviceCountHistory(models.Model):
    id =models.IntegerField(primary_key=True)
    devicecount = models.IntegerField()
    deviceonline = models.IntegerField()
    deviceoffline = models.IntegerField()
    date = models.DateTimeField(null=True)




    #老Flask模型,参考
    """ 
    id = db.Column(db.Integer,primary_key=True) 
    deviceip = db.Column(db.String(64),unique=True)#设备IP地址,不允许重复
    devicename = db.Column(db.String(64)) #设备名
    devicearea = db.Column(db.String(64)) #设备区域
    devicetype = db.Column(db.String(64)) #设备类型
    deviceport = db.Column(db.Integer) #设备端口
    devicestat = db.Column(db.Boolean) #设备状态,默认不在线
    devicerem = db.Column(db.String(128)) """