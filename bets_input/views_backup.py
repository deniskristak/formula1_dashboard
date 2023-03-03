# # -*- coding: utf-8 -*-
# from django.shortcuts import render, get_object_or_404
#
# from .forms import F1DriversForm
# from .models import RaceBet, Race, Player
#
#
# def index(request):
#     return render(request, 'bets_index.html', {'form': F1DriversForm})
#
#
# def ordering(request):
#     current_player: Player = request.POST.get('player_formfield')
#     current_race: Race = request.POST.get('race_formfield')
#     type_of_race = request.POST.get('race_type_formfield')
#     bets = RaceBet.objects.filter(player=current_player, race=current_race)
#     print(type_of_race)
#     return render(request, 'ordering.html', {'bets': bets, 'current_player': current_player, 'current_race': current_race, 'type_of_race': type_of_race})
#
#
# def sort(request):
#     drivers_pks_ordered: list = request.POST.getlist('driver_order')
#     current_race: list = request.POST.get('current_race')
#     current_player: list = request.POST.get('current_player')
#     type_of_race = request.POST.get('type_of_race')
#     bets = []
#     for driver_pk in drivers_pks_ordered:
#         bet = RaceBet.objects.get(race=current_race, player=current_player, driver=driver_pk)
#         if type_of_race == 'race':
#             bet.position = drivers_pks_ordered.index(driver_pk) + 1
#         elif type_of_race == 'quali':
#             bet.position_quali = drivers_pks_ordered.index(driver_pk) + 1
#         print(bet)
#         bet.save()
#         bets.append(bet)
#     return render(request, 'sortable_drivers.html', {'bets': bets, 'current_race': current_race, 'current_player': current_player, 'type_of_race': type_of_race})
