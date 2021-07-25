from django.http import HttpResponse
from django.shortcuts import render, redirect

from choicepoll.models import Choice
from .models import PlayStatus

from music.models import SpotifyUser, Device

def index(request):
    if (request.user.is_superuser):
        if SpotifyUser.objects.count() > 0 and PlayStatus.objects.count() > 0:
            context = {
                "spotifyuser" : SpotifyUser.objects.get(pk=1),
                "playstatus" : PlayStatus.objects.get(pk=1),
                "devices" : Device.objects.all(),
            }
            return render(request, 'main/admin.html', context)
        return render(request, 'main/admin.html')
    elif (request.user.is_authenticated):
        return redirect("guest-index")
    else:
        return redirect("guest-index")


def startApp(request):
    state = PlayStatus(pk=1)
    state.startVotingThread()
    return redirect("main-index")

def stopApp(request):
    state = PlayStatus(pk=1, isPlaying=False)
    state.stopVotingThread()
    return redirect("main-index")


def getDevices(request):
    spotifyUser = SpotifyUser.objects.get(pk=1)
    spotifyUser.getDevices()
    return redirect("main-index")

def useDevice(request):
    state = PlayStatus(pk=1)
    state.targetDevice=request.POST["selected_device"]
    state.save()
    return redirect("main-index")

def getPlaylist(request):
    spotifyUser = SpotifyUser.objects.get(pk=1)
    spotifyUser.updatePlaylist()
    return redirect("main-index")

def updateStatus(request):
    state = PlayStatus(pk=1)
    state.resynchronize()
    return redirect("main-index")

def refreshToken(request):
    spotifyUser = SpotifyUser.objects.get(pk=1)
    spotifyUser.refreshToken()
    return redirect("main-index")

def unplaySongs(request):
    spotifyUser = SpotifyUser.objects.get(pk=1)
    spotifyUser.resetAllSongPlayedStatus()
    return redirect("main-index")