from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='vote-index'),
    path('detail/', views.detail, name='detail'),
    path('results/', views.results, name='results'),
    path('vote/', views.vote, name='vote'),
]
