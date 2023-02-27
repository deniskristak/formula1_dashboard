from django.urls import path

from . import views

app_name = 'tips_input'

urlpatterns = [
    path('', views.index, name='index'),
    path('tips_input/ordering/', views.ordering, name='ordering'),
    path('sort/', views.sort, name='sort'),
    path('tips_input/', views.tips_input, name='tips_input'),
]
