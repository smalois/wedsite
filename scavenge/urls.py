from django.urls import path                                                                                                                                                                   
                                                                                                                                                                                               
from . import views                                                                                                                                                                            
                                                                                                                                                                                               
urlpatterns = [                                                                                                                                                                                
    path('', views.index, name='scavenge-index'),                                                                                                                                                       
    path('aggv51pm', views.stage_one, name='scavenge-1'),                                                                                                                 
]     