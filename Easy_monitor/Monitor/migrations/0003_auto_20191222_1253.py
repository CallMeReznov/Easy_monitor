# Generated by Django 3.0 on 2019-12-22 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0002_deviceinfo_deviceadt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinfo',
            name='deviceadt',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='设备添加时间'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='devicearea',
            field=models.CharField(max_length=64, verbose_name='设备区域'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='deviceip',
            field=models.CharField(max_length=64, unique=True, verbose_name='设备地址'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='devicename',
            field=models.CharField(max_length=64, verbose_name='设备名称'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='deviceport',
            field=models.IntegerField(verbose_name='设备端口'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='devicerem',
            field=models.CharField(max_length=256, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='devicestat',
            field=models.BooleanField(verbose_name='设备状态'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='devicetype',
            field=models.CharField(max_length=64, verbose_name='设备类型'),
        ),
    ]
