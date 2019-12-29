# Generated by Django 3.0 on 2019-12-29 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0008_devicecounthistory_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinfo',
            name='deviceid',
            field=models.IntegerField(default=1, primary_key=True, serialize=False, verbose_name='设备序号'),
        ),
        migrations.AlterField(
            model_name='deviceinfo',
            name='devicerem',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='备注'),
        ),
    ]