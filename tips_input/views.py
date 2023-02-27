# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from .forms import F1DriversForm
from .models import RaceTip, Race, Player

def index(request):
    return render(request, 'tips_index.html', {'form': F1DriversForm})


def ordering(request):
    current_player: Player = request.POST.get('player_formfield')
    current_race: Race = request.POST.get('race_formfield')
    type_of_race = request.POST.get('race_type_formfield')
    if type_of_race == 'race':
        tips = RaceTip.objects.filter(player=current_player, race=current_race)
    elif type_of_race == 'quali':
        tips = RaceTip.objects.filter(player=current_player, race=current_race).order_by('position_quali')
    return render(request, 'ordering.html', {'tips': tips, 'current_player': current_player, 'current_race': current_race, 'type_of_race': type_of_race})


def sort(request):
    drivers_pks_ordered: list = request.POST.getlist('driver_order')
    current_race: list = request.POST.get('current_race')
    current_player: list = request.POST.get('current_player')
    type_of_race = request.POST.get('type_of_race')
    tips = []
    for driver_pk in drivers_pks_ordered:
        tip = RaceTip.objects.get(race=current_race, player=current_player, driver=driver_pk)
        if type_of_race == 'race':
            tip.position = drivers_pks_ordered.index(driver_pk) + 1
        elif type_of_race == 'quali':
            tip.position_quali = drivers_pks_ordered.index(driver_pk) + 1
        print(tip)
        tip.save()
        tips.append(tip)
    return render(request, 'sortable_drivers.html', {'tips': tips, 'current_race': current_race, 'current_player': current_player, 'type_of_race': type_of_race})
