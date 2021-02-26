
from django.urls import path

from . import views

urlpatterns = [
    path('spotifyLogin/', views.spotifyLogin, name='spotify-login'),
    path('tokenRequest/', views.tokenRequest, name='token-request'),
    path('nowPlaying/', views.nowPlaying, name='music-playing'),
]