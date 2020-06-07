from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alarms/add', views.alarms_add, name='alarms_add'),
    path('alarms/list', views.alarms_list, name='alarms_list'),
    path('alarms/remove', views.alarms_remove, name='alarms_remove'),
    path('datetime/set', views.datetime_set, name='datetime_set'),
    path('manage/reboot', views.reboot, name='reboot'),
    path('manage/reset', views.factory_reset, name='reset')
]