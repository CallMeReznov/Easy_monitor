# Generated by Django 3.0 on 2019-12-25 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0005_auto_20191222_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceCountHistory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('devicecount', models.IntegerField(max_length=10)),
                ('deviceonline', models.IntegerField(max_length=10)),
                ('deviceoffline', models.IntegerField(max_length=10)),
            ],
        ),
    ]
