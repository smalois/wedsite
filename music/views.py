from django.http import HttpResponse
from django.shortcuts import redirect, render
from music.models import SpotifyUser
from main.models import PlayStatus

from . import constants as music
from . import urls

from datetime import datetime, timedelta
import requests
import json

import urllib.parse

def spotifyLogin(request):
    return redirect(music.ENDPOINT_AUTH + 
        '?response_type=code' + 
        '&client_id=' + music.CLIENT_ID + 
        '&scope=' + urllib.parse.quote_plus(music.SCOPES) + 
        '&redirect_uri=' + urllib.parse.quote_plus(music.REDIRECT))

def tokenRequest(request):
    code = request.GET.get("code", "")
    state  = request.GET.get("state", "")

    if (code == ""):
        return HttpResponse("No authentication code returned")
    else:
        header = {"Authorization": "Basic " + music.ENCODED_PAIR}
        data = {"grant_type":"authorization_code", 
            "code": code, 
            "redirect_uri":music.REDIRECT}

        response = requests.post(music.ENDPOINT_TOKEN, data = data, headers = header)

        if (response.ok):
            access_token = response.json()["access_token"]
            refresh_token = response.json()["refresh_token"]
            expiration_date = datetime.now() + timedelta(seconds=int(response.json()["expires_in"]))
            scope = response.json()["scope"]

            playerAccount = SpotifyUser(id=1, access_token=access_token, expiration_date=expiration_date, refresh_token=refresh_token, scope=scope)
            playerAccount.save()
            return redirect("main-index")
        return HttpResponse("failed")

def nowPlaying(request):
    playingStatus = PlayStatus.objects.get(pk=1)
    context = {
        'song': playingStatus.currentSong,
        'playing': playingStatus.isPlaying,
    }

    return render(request, "music/index.html", context)