from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main-index'),
    path('startApp', views.startApp, name='Start'),
    path('stopApp', views.stopApp, name='Stop'),
    path('getDevices', views.getDevices, name='get-devices'),
    path('useDevice', views.useDevice, name='use-device'),
    path('getPlaylist', views.getPlaylist, name='get-playlist'),
    path('updateStatus', views.updateStatus, name='update-progress'),
    path('unplaySongs', views.unplaySongs, name='unplaySongs'),
    path('refreshToken', views.refreshToken, name='refresh-token'),
]
