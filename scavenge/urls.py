from django.urls import path                                                                                                                                                                   
                                                                                                                                                                                               
from . import views                                                                                                                                                                            
                                                                                                                                                                                               
urlpatterns = [                                                                                                                                                                                
    path('', views.index, name='scavenge-index'),                                                                                                                                                       
    # path('scavenge_1', views.index, name='scavenge-1'),                                                                                                                 
]     