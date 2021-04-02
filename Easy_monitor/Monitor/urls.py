from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('api/notfound',views.notfound,name='notfound'),
    path('api/notread',views.notread,name='notread'),
    path('history/<str:deviceip>',views.devicestathistory,name='history'),
    path('preview/<str:deviceip>',views.devicestatpreview,name='preview'),
]