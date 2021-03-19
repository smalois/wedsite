from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Choice
from . import urls

def index(request):
    selections = Choice.objects.all()                                                                                                                                                          
    context = {                                                                                                                                                                                
        'user': request.user,                                                                                                                                                                  
        'choices': selections,                                                                                                                                                                 
    }                                                                                                                                                                                          
    return render(request, 'choicepoll/index.html', context)   

def detail(request):
    return HttpResponse("Details page")

def results(request):
    selections = Choice.objects.all()
    context = {
        'choices': selections,
        'guest': request.user,
    }
    return render(request, 'choicepoll/results.html', context)

def vote(request):
    if (not (request.user.guest.hasVoted)):
        selected_choice = Choice.objects.get(pk=request.POST['choice'])
        if (selected_choice.voteEnabled):
            selected_choice.votes += 1
            request.user.guest.hasVoted = True
            selected_choice.save()
            request.user.guest.save()
    return HttpResponseRedirect(reverse('results'))