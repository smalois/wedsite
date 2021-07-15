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

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/one.html', context)

def stage_two(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[1] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/two.html', context)

def stage_three(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[2] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/three.html', context)

def stage_four(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[3] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/four.html', context)

def stage_five(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[4] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/five.html', context)

def stage_six(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[5] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/six.html', context)

def stage_seven(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[6] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/seven.html', context)

def stage_eight(request):
    if request.user.is_anonymous or (not request.user.is_authenticated):
        return render(request, 'scavenge/not_auth.html')
        
    progressString = request.user.guest.scavProgress 
    if progressString:
        tempList = list(progressString)
        tempList[7] = '1'
        request.user.guest.scavProgress = ''.join(tempList)
    else:
        request.user.guest.scavProgress = '1000000000000000'

    context = {
        'progress0' : request.user.guest.scavProgress[0], 
        'progress1' : request.user.guest.scavProgress[1], 
        'progress2' : request.user.guest.scavProgress[2], 
        'progress3' : request.user.guest.scavProgress[3], 
        'progress4' : request.user.guest.scavProgress[4], 
        'progress5' : request.user.guest.scavProgress[5], 
        'progress6' : request.user.guest.scavProgress[6], 
        'progress7' : request.user.guest.scavProgress[7], 
        'progress8' : request.user.guest.scavProgress[8], 
    }

    request.user.guest.save()
    return render(request, 'scavenge/eight.html', context)