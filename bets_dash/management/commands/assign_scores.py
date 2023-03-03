from django.core.management.base import BaseCommand, CommandError
from typing import Tuple
import logging

# import any model you need:
from bets_input.models import Player, RaceBet, Race, Driver, Team
from bets_dash.models import Results, PlayerPoints

logging.basicConfig(filename='bets_dash/management/scores.log', filemode='w', level=logging.INFO)

def get_results(results : Results) -> Tuple[list, str, str, set]:
    """ Store results in python arrays.
    
    Parameters
    ----------
    results : Results

    Returns
    -------
    sorted_drivers : lst
    dotd : str 
    fastest_lap : str
    dnfs : set
    """

    truelist = []
    dnfs = []
    for result in results:
        truelist.append([
                result.driver.name,
                result.position
            ])
        if result.dotd:
            dotd = result.driver.name
        if result.fastest_lap:
            fasttest_lap = result.driver.name
        if result.dnf:
            dnfs.append(result.driver.name)

    # sort the list 
    truelist.sort(key = lambda x: x[1])
    sorted_drivers = [x[0] for x in truelist]
    dnfs = set(dnfs)
    return sorted_drivers, dotd, fasttest_lap, dnfs

def score_player(bet : RaceBet, results : Results) -> int:
    """ Score a player's bet against truth.

    Parameters
    ----------
    bet : Racebet
    results : Results
    
    Returns
    -------
    score : int
    """

    drivers_sorted, dotd, fastest_lap, dnfs = get_results(results)
    score = 0

    dnfsplayer = []
    for betrow in bet:
        dname = betrow.driver.name
        dpos = betrow.position - 1 
        if dname == drivers_sorted[dpos]:
            score += 5
        elif dpos != 0:
            if dname == drivers_sorted[dpos-1]:
                score += 2 
        elif dpos != 19:
            if dname == drivers_sorted[dpos+1]:
                score += 2
        elif dpos not in [0,1]:
            if dname == drivers_sorted[dpos-2]:
                score += 1
        elif dpos not in [18,19]:
            if dname == drivers_sorted[dpos+2]:
                score += 1
        if betrow.dotd:
            if dname == dotd:
                score += 1
        if betrow.fastest_lap:
            if dname == fastest_lap:
                score += 1
        if betrow.dnf:
            dnfsplayer.append(dname)
    
    dnfsplayer = set(dnfsplayer)
    # compare sets of true and predicted dnfs 
    # add size of the intersection to the tally (max 5 points)
    score += min(len(dnfsplayer.intersection(dnfs)), 5)

    return score

# run with `pyhon manage.py edov_cmd`
class Command(BaseCommand):
    help = 'nech boh posudi jak kto a kde co'
    # in this method, you write what the cmd should do
    def handle(self, *args, **options):

        #TODO put this in arguments

        races = Race.objects.all()
        for race in races:
            # results = Results.objects.get(race=race)
                    # # for now
            my_player = Player.objects.get(nickname='tomasko')
            results = Results.objects.filter(
                    race=race
            )

            # scoring for each of the players in db
            for player in Player.objects.all():
                playersbet = RaceBet.objects.filter(
                    race=race,
                    player=player
                )
                score = score_player(playersbet, results)
                logging.info(f"{player.fullname} : {score}")
                # save the data
                PlayerPoints.objects.filter(player=player, race=race).delete()
                PlayerPoints.objects.create(
                    player=player,
                    race=race,
                    points=score
                )