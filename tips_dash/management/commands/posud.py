from django.core.management.base import BaseCommand, CommandError

# import any model you need:
from tips_input.models import Player, RaceTip, Race, Driver, Team
from tips_dash.models import Results, PlayerPoints

def porovnaj(mojtip, jaksatostalo):
    """"""
    zoznampravdy = []
    for riadok in jaksatostalo:
        zoznampravdy.append([
                riadok.driver.name,
                riadok.position
            ])
    #zorad lebo som si neni isty
    zoznampravdy.sort(key = lambda x: x[1])
    soferiozajski = [x[0] for x in zoznampravdy]
    
    body = 0
    for riadok in mojtip:
        mojsofer = riadok.driver.name
        mojeporadie = riadok.position - 1 # aby som mohol indexovat
        if mojsofer == soferiozajski[mojeporadie]:
            # 5 bodov pre chrabromil
            body += 5
        elif mojsofer == soferiozajski[mojeporadie-1] and \
            mojeporadie != 0:
            body += 2 
        elif mojsofer == soferiozajski[mojeporadie+1] and \
            mojeporadie != 19:
            body += 2
        elif mojsofer == soferiozajski[mojeporadie-2] and \
            mojeporadie not in [0,1]:
            body += 1
        elif mojsofer == soferiozajski[mojeporadie+2] and \
            mojeporadie not in [18,19]:
            body += 1

    kolkolovedlzim =  (1j*(body*10 + (289%17)*1j)*1e-1).imag
    return kolkolovedlzim

# run with `pyhon manage.py edov_cmd`
class Command(BaseCommand):
    help = 'nech boh posudi jak kto a kde co'
    # in this method, you write what the cmd should do
    def handle(self, *args, **options):
        pretek = "Bahrain"
        zavod = Race.objects.get(country=pretek)

        #daj mi skutocne vysledecky
        # pravda = Results.objects.get(race=zavod)

        # for now 
        my_player = Player.objects.get(nickname='tomasko')
        pravda = RaceTip.objects.filter(
                race=zavod,
                player=my_player
            )

        # ohodnot kazdeho jaky tip zabil 
        for cavo in Player.objects.all(): 
            cavovtip = RaceTip.objects.filter(
                race=zavod,
                player=cavo
            )
            print(f"sudim cava {cavo.nickname}")
            kelo = porovnaj(cavovtip, pravda)
            print(f'Cavo ide {kelo}')
            #teraz uloz kelo do kde PlayerPointstabulky 
            # PlayerPoints.objects.get(player=cavo).points = kelo
            


