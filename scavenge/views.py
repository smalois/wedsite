from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'scavenge/index.html')

def stage_one(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[0] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    request.user.guest.save()
    return render(request, 'scavenge/one.html')
