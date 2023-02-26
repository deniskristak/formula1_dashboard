from django.urls import path, include

from . import views

app_name = 'tips_input'

urlpatterns = [
    path('', views.index, name='index'),
    path('ordering/', views.ordering, name='ordering'),
    path('sort/', views.sort, name='sort'),
]
