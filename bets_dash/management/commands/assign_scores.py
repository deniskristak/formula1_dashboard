from django.core.management.base import BaseCommand, CommandError
from typing import Tuple
import logging

# import any model you need:
from bets_input.models import Player, RaceBet, Race, PlayerPlacedBet
from bets_dash.models import Results, PlayerPoints

logging.basicConfig(
    filename="bets_dash/management/scores.log", filemode="w", level=logging.INFO
)


def get_results(results: Results) -> Tuple[list, str, str, set]:
    """Store results in python arrays.

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

    truelist_quali = [
        [result.driver.name, result.position_sprint] for result in results
    ]
    truelist_sprint = [
        [result.driver.name, result.position_sprint] for result in results
    ]
    truelist_gp = [[result.driver.name, result.position] for result in results]
    # truelist_quali = truelist_sprint = truelist_gp
    dnfs = [result.driver.name for result in results if result.dnf]
    dotd = [result.driver.name for result in results if result.dotd][0]
    fastest_lap = [result.driver.name for result in results if result.fastest_lap][0]
    # sort because I am not sure if sorted in db
    truelist_quali.sort(key=lambda x: x[1])
    truelist_sprint.sort(key=lambda x: x[1])
    truelist_gp.sort(key=lambda x: x[1])
    # encapsulate orders in lists
    sorted_drivers = [
        [x[0] for x in truelist_quali],
        [x[0] for x in truelist_sprint],
        [x[0] for x in truelist_gp],
    ]
    dnfs = set(dnfs)
    return sorted_drivers, dotd, fastest_lap, dnfs


def score_order(driver_name, dpos, drivers_sorted, weights):
    """Score the order.

    Parameters:
    -----------
    driver_name : string
    dpos : int
    drivers_sorted : list of true results with drivers' names
    weights : (nx3) array

    Returns
    -----------
    score : int
    """

    big, medium, small = weights
    score = 0

    if dpos:
        idx = dpos - 1
        if driver_name == drivers_sorted[idx]:
            score += big
        elif dpos != 0:
            if driver_name == drivers_sorted[idx - 1]:
                score += big
        elif dpos != 19:
            if driver_name == drivers_sorted[idx + 1]:
                score += medium
        elif dpos not in [0, 1]:
            if driver_name == drivers_sorted[idx - 2]:
                score += small
        elif dpos not in [18, 19]:
            if driver_name == drivers_sorted[idx + 2]:
                score += small
    return score


def score_player(bet: RaceBet, results: Results) -> int:
    """Score a player's bet against truth.

    Parameters
    ----------
    bet : RaceBet
    results : Results

    Returns
    -------
    score : int
    """

    d_sorted, dotd, fastest_lap, dnfs = get_results(results)
    score = 0

    dnfsplayer = []
    for betrow in bet:
        dname = betrow.driver.name

        score += score_order(
            driver_name=dname,
            dpos=betrow.position_quali,
            drivers_sorted=d_sorted[0],
            weights=[1, 0, 0],
        )
        score += score_order(
            driver_name=dname,
            dpos=betrow.position_sprint,
            drivers_sorted=d_sorted[1],
            weights=[2, 1, 0],
        )
        score += score_order(
            driver_name=dname,
            dpos=betrow.position,
            drivers_sorted=d_sorted[2],
            weights=[5, 2, 1],
        )

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


class Command(BaseCommand):
    # in this method, you write what the cmd should do
    def handle(self, *args, **options):
        races = Race.objects.all()
        for race in races:
            results = Results.objects.filter(race=race)

            # scoring for each of the players in db
            for player in Player.objects.all():
                playersbet = RaceBet.objects.filter(race=race, player=player)
                score = score_player(playersbet, results)
                logging.info(f"{player.fullname} : {score}")
                # save the data
                PlayerPoints.objects.filter(player=player, race=race).delete()
                PlayerPoints.objects.create(player=player, race=race, points=score)
