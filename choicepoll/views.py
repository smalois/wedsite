from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone 
from .models import Choice
from main.models import PlayStatus
from music import constants
from . import urls


def index(request):
    selections = Choice.objects.all()                                                                                                                                                          
    playStatus = PlayStatus.objects.get(pk=1)
    songTimeRemaining = playStatus.songEndTime - timezone.now()
    votingTimeRemaining = songTimeRemaining - timezone.timedelta(seconds=constants.VOTE_TRANSITION_SECONDS)
    context = {                                                                                                                                                                                
        'user': request.user,                                                                                                                                                                  
        'choices': selections,                                                                                                                                                                 
        'playing': playStatus.isPlaying,
        'voteTimeRemaining': votingTimeRemaining.seconds,
        'songTimeRemaining': songTimeRemaining.seconds,
    }                                                                                                                                                                                          
    return render(request, 'choicepoll/index.html', context)   

def detail(request):
    return HttpResponse("Details page")

def results(request):
    selections = Choice.objects.all()
    playStatus = PlayStatus.objects.get(pk=1)
    context = {
        'choices': selections,
        'guest': request.user,
        'playStatus': playStatus,
    }
    return render(request, 'choicepoll/results.html', context)

def vote(request):
    if (not (request.user.guest.hasVoted)):
        selected_choice = Choice.objects.get(pk=request.POST['choice'])
        if (selected_choice.voteEnabled):
            selected_choice.votes += 1
            if (not request.user.username == "MusicLaptop"):
                request.user.guest.hasVoted = True
                request.user.guest.save()
            selected_choice.save()

    if (not request.user.username == "MusicLaptop"):
        return HttpResponseRedirect(reverse('results'))
    else:
        return render(request, 'choicepoll/laptop_wait.html')

def laptop_wait(request):
    return render(request, 'choicepoll/laptop_wait.html')