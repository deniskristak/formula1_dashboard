# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect

from .forms import F1DriversForm, DriverExtrasForm
from .models import RaceTip, Race, Player


def index(request):
    form = F1DriversForm()
    return render(request, 'tips_index.html', {'form': form})


def ordering(request):
    # we access the post data from previous view if we were only redirected to this view
    if '_old_post' in request.session.keys():
        request.POST = request.session['_old_post']
        # todo: if quali page is refreshed, browser cannot access data from this _old_post since we're deleting it - try to think about a solution
        request.session.pop('_old_post')
    current_player: Player = request.POST.get('player_formfield')
    current_race: Race = request.POST.get('race_formfield')
    race_type = request.POST.get('race_type_formfield')
    if race_type == 'race':
        tips = RaceTip.objects.filter(player=current_player, race=current_race)
        # reset player's tips about dnf, dotd, fastest_lap
        all_drivers_tips = RaceTip.objects.filter(player=current_player, race=current_race)
        for tip in all_drivers_tips:
            tip.dnf = False
            tip.fastest_lap = False
            tip.dotd = False
            tip.save()

        # if we are on race, there are data in request with info about dnf, dotd, fastest_lap
        # update dnf, fastest_lap and dotd according to the selection from previous page
        dnf_driver_1 = RaceTip.objects.get(player=current_player, race=current_race, driver=request.POST.get('dnf_select_1'))
        dnf_driver_1.dnf = True
        dnf_driver_1.save()
        dnf_driver_2 = RaceTip.objects.get(player=current_player, race=current_race, driver=request.POST.get('dnf_select_2'))
        dnf_driver_2.dnf = True
        dnf_driver_2.save()
        dnf_driver_3 = RaceTip.objects.get(player=current_player, race=current_race, driver=request.POST.get('dnf_select_3'))
        dnf_driver_3.dnf = True
        dnf_driver_3.save()
        dotd_driver = RaceTip.objects.get(player=current_player, race=current_race, driver=request.POST.get('dotd_select'))
        dotd_driver.dotd = True
        dotd_driver.save()
        fastest_lap_driver = RaceTip.objects.get(player=current_player, race=current_race, driver=request.POST.get('fastest_lap_select'))
        fastest_lap_driver.fastest_lap = True
        fastest_lap_driver.save()

    elif race_type == 'quali':
        tips = RaceTip.objects.filter(player=current_player, race=current_race).order_by('position_quali')
    form = DriverExtrasForm(curr_player=current_player, curr_race=current_race, race_type=race_type)
    return render(
        request,
        'ordering.html',
        {
            'tips': tips,
            'current_player': current_player,
            'current_race': current_race,
            'race_type': race_type,
            'form': form,
        },
    )


def tips_input(request):
    current_player: Player = request.POST.get('player_formfield')
    current_race: Race = request.POST.get('race_formfield')
    race_type = request.POST.get('race_type_formfield')
    if race_type == 'quali':
        request.session['_old_post'] = request.POST
        return redirect('/tips_input/ordering/')
    elif race_type == 'race':
        tips = RaceTip.objects.filter(player=current_player, race=current_race)
    form = DriverExtrasForm(curr_player=current_player, curr_race=current_race, race_type=race_type)
    return render(
        request,
        'extras_input.html',
        {
            'tips': tips,
            'current_player': current_player,
            'current_race': current_race,
            'race_type': race_type,
            'form': form,
        },
    )


def sort(request):
    drivers_pks_ordered: list = request.POST.getlist('driver_order')
    current_race: list = request.POST.get('current_race')
    current_player: list = request.POST.get('current_player')
    race_type = request.POST.get('race_type')
    tips = []
    for driver_pk in drivers_pks_ordered:
        tip = RaceTip.objects.get(race=current_race, player=current_player, driver=driver_pk)
        if race_type == 'race':
            tip.position = drivers_pks_ordered.index(driver_pk) + 1
        elif race_type == 'quali':
            tip.position_quali = drivers_pks_ordered.index(driver_pk) + 1
        tip.save()
        tips.append(tip)
    return render(
        request,
        'sortable_drivers.html',
        {'tips': tips, 'current_race': current_race, 'current_player': current_player, 'race_type': race_type})
