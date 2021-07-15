from django.urls import path                                                                                                                                                                   
                                                                                                                                                                                               
from . import views                                                                                                                                                                            
                                                                                                                                                                                               
urlpatterns = [                                                                                                                                                                                
    path('', views.index, name='scavenge-index'),                                                                                                                                                       
    path('aggv51pm', views.stage_one, name='scavenge-1'),
    path('jonowyfj', views.stage_two, name='scavenge-2'),
    path('axylehdi', views.stage_three, name='scavenge-3'),
    path('nlgyrzeh', views.stage_four, name='scavenge-4'),
    path('snkeynjb', views.stage_five, name='scavenge-5'),
    path('omtigdom', views.stage_six, name='scavenge-6'),
    path('clue_7', views.stage_seven, name='scavenge-7'),
    path('clue_8', views.stage_eight, name='scavenge-8'),
]     