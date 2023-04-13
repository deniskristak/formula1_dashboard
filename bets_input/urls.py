from django.urls import path

from . import views

app_name = 'bets_input'

urlpatterns = [
    path('', views.index, name='index'),
    path('bets_input/ordering/', views.ordering, name='ordering'),
    path('sort/', views.sort, name='sort'),
    path('bets_input/', views.bets_input, name='bets_input'),
]
