from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main-index'),
    path('startApp', views.startApp, name='Start'),
    path('stopApp', views.stopApp, name='Stop'),
    path('getDevices', views.getDevices, name='get-devices'),
    path('getPlaylist', views.getPlaylist, name='get-playlist'),
]
