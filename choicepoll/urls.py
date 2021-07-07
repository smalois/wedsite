from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='vote-index'),
    path('detail/', views.detail, name='detail'),
    path('results/', views.results, name='results'),
    path('wait/', views.laptop_wait, name='laptop_wait'),
    path('vote/', views.vote, name='vote'),
]
