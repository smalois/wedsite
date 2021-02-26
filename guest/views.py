from django.http import HttpResponse                                                                                                                                                           
from django.shortcuts import render, redirect                                                                                                                                                  
from django.contrib.auth import authenticate, login                                                                                                                                            
                                                                                                                                                                                               
def index(request):                                                                                                                                                                            
    context = {                                                                                                                                                                                
        'user': request.user,                                                                                                                                                                  
    }                                                                                                                                                                                          
    return render(request, 'guest/index.html', context)                                                                                                                                        
                                                                                                                                                                                               
def guest_id(request, guest_name, guest_id):                                                                                                                                                   
    user = authenticate(username=guest_name, password=guest_id)                                                                                                                                
    if user is not None:                                                                                                                                                                       
        login(request, user)                                                                                                                                                                   
        return redirect('/guest/')                                                                                                                                                            
    else:                                                                                                                                                                                      
        return HttpResponse("Guest %s id %s not found" % (guest_name , guest_id))