from django.urls import path                                                                                                                                                                   
                                                                                                                                                                                               
from . import views                                                                                                                                                                            
                                                                                                                                                                                               
urlpatterns = [                                                                                                                                                                                
    path('', views.index, name='guest-index'),                                                                                                                                                       
    path('<str:guest_name>/<str:guest_id>/', views.guest_id, name='guest_id'),                                                                                                                 
]     