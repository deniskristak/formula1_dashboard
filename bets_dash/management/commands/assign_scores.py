from django.core.management.base import BaseCommand, CommandError
from typing import Tuple
import logging

from django.db.models import QuerySet

# import any model you need:
from bets_input.models import Player, RaceBet, Race, PlayerPlacedBet
from bets_dash.models import Results, PlayerPoints, PlayerPointsTotal

logging.basicConfig(
    filename="bets_dash/management/scores.log", filemode="w", level=logging.INFO
)


def get_results(results: list[Results]) -> Tuple[list, str, str, set, set]:
    """Store results in python arrays.

    Parameters
    ----------
    results : list[Results]

    Returns
    -------
    sorted_drivers : lst
    dotd : str
    fastest_lap : str
    dnfs_race : set
    dnfs_sprint: set
    """

    truelist_quali = [
        [result.driver.name, result.position_sprint] for result in results
    ]
    truelist_sprint = [
        [result.driver.name, result.position_sprint] for result in results
    ]
    truelist_race = [[result.driver.name, result.position] for result in results]
    dnfs_race = [result.driver.name for result in results if result.dnf]
    dnfs_sprint = [result.driver.name for result in results if result.dnf_sprint]
    dotd = [result.driver.name for result in results if result.dotd][0]
    fastest_lap = [result.driver.name for result in results if result.fastest_lap][0]
    # sort because I am not sure if sorted in db
    truelist_quali.sort(key=lambda x: x[1])
    truelist_sprint.sort(key=lambda x: x[1])
    truelist_race.sort(key=lambda x: x[1])
    # encapsulate orders in lists
    sorted_drivers = [
        [x[0] for x in truelist_quali],
        [x[0] for x in truelist_sprint],
        [x[0] for x in truelist_race],
    ]
    dnfs_race = set(dnfs_race)
    dnfs_sprint = set(dnfs_sprint)

    return (
        sorted_drivers,
        dotd,
        fastest_lap,
        dnfs_race,
        dnfs_sprint,
    )


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


def score_player(
    bet: RaceBet,
    results: list[Results],
    race_is_sprint: bool,
    bets_placed_per_racetype: QuerySet[PlayerPlacedBet],
) -> tuple[int, int, int]:
    """Score a player's bet against truth.

    Parameters
    ----------
    :param bet : RaceBet
    :param results : list[Results]

    :return
    -------
    score : int
    score_sprint: int
    score_quali: int
    """

    drivers_sorted, dotd, fastest_lap, dnfs_race, dnfs_sprint = get_results(results)
    score_quali = 0
    score_sprint = 0
    score_race = 0

    dnfsplayer_sprint = []
    dnfsplayer_race = []
    for betrow in bet:
        driver_name = betrow.driver.name

        score_quali += score_order(
            driver_name=driver_name,
            dpos=betrow.position_quali,
            drivers_sorted=drivers_sorted[0],
            weights=[1, 0, 0],
        )
        # check if race is sprint before doing any evaluation
        if race_is_sprint:
            score_sprint += score_order(
                driver_name=driver_name,
                dpos=betrow.position_sprint,
                drivers_sorted=drivers_sorted[1],
                weights=[2, 1, 0],
            )
            # this
            if betrow.dnf_sprint:
                dnfsplayer_sprint.append(driver_name)
        score_race += score_order(
            driver_name=driver_name,
            dpos=betrow.position,
            drivers_sorted=drivers_sorted[2],
            weights=[5, 2, 1],
        )
        if betrow.dotd:
            if driver_name == dotd:
                score_race += 1
        if betrow.fastest_lap:
            if driver_name == fastest_lap:
                score_race += 1
        if betrow.dnf:
            dnfsplayer_race.append(driver_name)

    # compare sets of true and predicted dnfs
    # add size of the intersection to the tally (max 5 points)
    score_race += min(len(set(dnfsplayer_race).intersection(dnfs_race)), 5)
    # same for sprint, but only if applicable
    if race_is_sprint:
        score_sprint += min(len(set(dnfsplayer_sprint).intersection(dnfs_sprint)), 5)

    # todo this method is too big now, would be nice to tidy up
    # in case the player didn't register the bet (there are just defaults), we set respective points gained to 0
    if bets_placed_per_racetype.filter(race_type="quali").count() == 0:
        score_quali = 0
    if bets_placed_per_racetype.filter(race_type="sprint").count() == 0:
        score_sprint = 0
    if bets_placed_per_racetype.filter(race_type="race").count() == 0:
        score_race = 0

    return score_race, score_sprint, score_quali


class Command(BaseCommand):
    # in this method, you write what the cmd should do
    def handle(self, *args, **options):
        PlayerPoints.objects.all().delete()
        PlayerPointsTotal.objects.all().delete()
        races = Race.objects.all()
        for race in races:
            race_is_sprint = race.is_sprint
            results = Results.objects.filter(race=race)

            # scoring for each of the players in db
            for player in Player.objects.all():
                playersbet = RaceBet.objects.filter(race=race, player=player)
                bets_placed_per_racetype = PlayerPlacedBet.objects.filter(
                    race=race, player=player
                )
                score_race, score_sprint, score_quali = score_player(
                    playersbet, results, race_is_sprint, bets_placed_per_racetype
                )

                logging.info(
                    f"{player.fullname} : {score_race}"
                )  # todo add more details + print msg

                # save the data
                PlayerPoints.objects.create(
                    player=player,
                    race=race,
                    points_race=score_race,
                    points_sprint=score_sprint,
                    points_quali=score_quali,
                )
                points_total, _ = PlayerPointsTotal.objects.get_or_create(player=player)
                points_total.points_total += score_race + score_sprint + score_quali
                points_total.save()
