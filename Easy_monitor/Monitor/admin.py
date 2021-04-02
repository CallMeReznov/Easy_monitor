
from django.contrib import admin
from .models import DeviceInfo
from django.utils.html import format_html
# Register your models here.

@admin.register(DeviceInfo)
class Newadmin(admin.ModelAdmin):

    list_display = ('deviceid','devicename','deviceip','devicearea','devicetype','devicestat','deviceport','deviceadt','preview','devicerem','history')
    date_hierarchy = 'deviceadt'
    list_editable =['devicerem']
    list_per_page=100
    search_fields = ['devicename', 'deviceip','devicetype','devicearea']
    list_display_links=('devicename','deviceip')
    readonly_fields = ('deviceid',)
    


#admin.site.site_title = ''
#admin.site.site_header = ''