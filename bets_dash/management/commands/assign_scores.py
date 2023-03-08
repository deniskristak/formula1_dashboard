from django.core.management.base import BaseCommand, CommandError
from typing import Dict, List, Set
import logging

# import any model you need:
from bets_input.models import Player, RaceBet, Race, PlayerPlacedBet
from bets_dash.models import (
    Results,
    PlayerPoint,
    PlayerPointsTotal,
    EventAssessmentStatus,
)

logging.basicConfig(
    filename="bets_dash/management/scores.log", filemode="w", level=logging.INFO
)


def transform_results(
    results: List[Results],
) -> Dict[str, List[str | int] | str | set[str]]:
    """Store results in python arrays.

    Parameters
    ----------
    results : List[Results]

    Returns
    -------
    sorted_drivers_quali: List
    sorted_drivers_sprint: List
    sorted_drivers_race : lst
    dotd : str
    fastest_lap : str
    dnfs_race : set
    dnfs_sprint: set
    """

    truelist_quali = [[result.driver.name, result.position_quali] for result in results]
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

    sorted_drivers_quali = [x[0] for x in truelist_quali]
    sorted_drivers_sprint = [x[0] for x in truelist_sprint]
    sorted_drivers_race = [x[0] for x in truelist_race]

    dnfs_race = set(dnfs_race)
    dnfs_sprint = set(dnfs_sprint)
    results_per_weekend = {
        "sorted_drivers_quali": sorted_drivers_quali,
        "sorted_drivers_sprint": sorted_drivers_sprint,
        "sorted_drivers_race": sorted_drivers_race,
        "dotd": dotd,
        "fastest_lap": fastest_lap,
        "dnfs_race": dnfs_race,
        "dnfs_sprint": dnfs_sprint,
    }

    return results_per_weekend


# todo: mistake is probably here, since t19829962his method keeps printing weird points
def score_order(driver_name, dpos, drivers_sorted, weights):
    """Score the order.

    Parameters:
    -----------
    driver_name : string
    dpos : int
    drivers_sorted : List of true results with drivers' names
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
        if idx != 0:
            if driver_name == drivers_sorted[idx - 1]:
                score += medium
        if idx != 19:
            if driver_name == drivers_sorted[idx + 1]:
                score += medium
        if idx not in [0, 1]:
            if driver_name == drivers_sorted[idx - 2]:
                score += small
        if idx not in [18, 19]:
            if driver_name == drivers_sorted[idx + 2]:
                score += small
    return score


def score_player_race(
    bets: List[RaceBet], drivers_sorted, dotd, fastest_lap, dnfs_race
) -> int:
    """Score a player's bet against truth.

    Parameters
    ----------
    :param bets : RaceBet
    :param results : List[Results]

    :return
    -------
    score : int
    """

    score = 0

    dnfsplayer_race = []
    for betrow in bets:
        driver_name = betrow.driver.name
        score += score_order(
            driver_name=driver_name,
            dpos=betrow.position,
            drivers_sorted=drivers_sorted,
            weights=[5, 2, 1],
        )
        if betrow.dotd:
            if driver_name == dotd:
                score += 1
        if betrow.fastest_lap:
            if driver_name == fastest_lap:
                score += 1
        if betrow.dnf:
            dnfsplayer_race.append(driver_name)

    score += min(len(set(dnfsplayer_race).intersection(dnfs_race)), 5)
    return score


def score_player_sprint(
    bets: List[RaceBet], drivers_sorted: List[str], dnfs_sprint: List[str]
) -> int:
    """Score a player's bet against truth.

    Parameters
    ----------
    :param bets : RaceBet
    :param drivers_sorted : List[str]
    :param dnfs_sprint: List[str]

    :return
    -------
    score : int
    """

    score = 0

    dnfsplayer_sprint = []
    for betrow in bets:
        driver_name = betrow.driver.name

        # check if race is sprint before doing any evaluation
        score += score_order(
            driver_name=betrow.driver.name,
            dpos=betrow.position_sprint,
            drivers_sorted=drivers_sorted,
            weights=[2, 1, 0],
        )
        if betrow.dnf_sprint:
            dnfsplayer_sprint.append(driver_name)

    # compare sets of true and predicted dnfs
    # add size of the intersection to the tally (max 5 points)
    score += min(len(set(dnfsplayer_sprint).intersection(dnfs_sprint)), 5)
    return score


def score_player_quali(bets: List[RaceBet], drivers_sorted: List[str]) -> int:
    """Score a player's bet against truth.

    Parameters
    ----------
    :param bets : List[RaceBet]
    :param drivers_sorted : List[str]

    :return
    -------
    score : int
    """

    score = 0
    for betrow in bets:
        betrow_score = score_order(
            driver_name=betrow.driver.name,
            dpos=betrow.position_quali,
            drivers_sorted=drivers_sorted,
            weights=[1, 0, 0],
        )
        score += betrow_score
    return score


def assess_bets_race(
    results,
    race,
):
    # scoring for each of the players in db
    for player in Player.objects.all():
        # first we transform data into more suitable structure
        results_transformed = transform_results(results)
        playersbets = RaceBet.objects.filter(race=race, player=player)

        # first we find out if player's bets are default values or not
        # if not, we assess them
        race_not_default = PlayerPlacedBet.objects.filter(
            race=race, player=player, race_type="race"
        ).exists()

        if race_not_default:
            score_race = score_player_race(
                bets=playersbets,
                drivers_sorted=results_transformed.get("sorted_drivers_race"),
                fastest_lap=results_transformed.get("fastest_lap"),
                dotd=results_transformed.get("dotd"),
                dnfs_race=results_transformed.get("dnfs_race"),
            )
        else:
            score_race = 0

        # save the data
        player_points, _ = PlayerPoint.objects.get_or_create(
            player=player,
            race=race,
        )
        player_points.points_race = score_race
        player_points.save()

        # add to competition's total points per player
        points_total, _ = PlayerPointsTotal.objects.get_or_create(player=player)
        points_total.points_total += score_race
        points_total.save()


def assess_bets_sprint(
    results,
    race,
):
    # first we transform data into more suitable structure
    results_transformed = transform_results(results)
    # scoring for each of the players in db
    for player in Player.objects.all():
        playersbets = RaceBet.objects.filter(race=race, player=player)

        # first we find out if player's bets are default values or not
        # if not, we assess them
        sprint_not_default = PlayerPlacedBet.objects.filter(
            race=race, player=player, race_type="sprint"
        ).exists()

        if sprint_not_default:
            score_sprint = score_player_sprint(
                bets=playersbets,
                drivers_sorted=results_transformed.get("sorted_drivers_sprint"),
                dnfs_sprint=results_transformed.get("dnfs_sprint"),
            )
        else:
            score_sprint = 0

        # save the data
        player_points, _ = PlayerPoint.objects.get_or_create(
            player=player,
            race=race,
        )
        player_points.points_sprint = score_sprint
        player_points.save()

        # add to competition's total points per player
        points_total, _ = PlayerPointsTotal.objects.get_or_create(player=player)
        points_total.points_total += score_sprint
        points_total.save()


def assess_bets_quali(
    results,
    race,
):
    # first we transform data into more suitable structure
    results_transformed = transform_results(results)
    # scoring for each of the players in db
    for player in Player.objects.all():
        playersbets = RaceBet.objects.filter(race=race, player=player)

        # first we find out if player's bets are default values or not
        # if not, we assess them
        quali_not_default = PlayerPlacedBet.objects.filter(
            race=race, player=player, race_type="quali"
        ).exists()

        if quali_not_default:
            score_quali = score_player_quali(
                bets=playersbets,
                drivers_sorted=results_transformed.get("sorted_drivers_quali"),
            )
        else:
            score_quali = 0

        # save the data
        player_points, _ = PlayerPoint.objects.get_or_create(
            player=player,
            race=race,
        )
        player_points.points_quali = score_quali
        player_points.save()

        # add to competition's total points per player
        points_total, _ = PlayerPointsTotal.objects.get_or_create(player=player)
        points_total.points_total += score_quali
        points_total.save()


class Command(BaseCommand):
    # this command calculates points for each player's bets for each race
    # however, it firstly checks whether the bet is a result of user input or whether it is a default value for bets
    # if race doesn't involve a sprint event, it will not be evaluated at all
    # todo debug - it's calculating nonsense (at quali)
    def handle(self, *args, **options):
        # first, we delete all data about points to avoid duplication
        PlayerPoint.objects.all().delete()
        PlayerPointsTotal.objects.all().delete()
        EventAssessmentStatus.objects.all().delete()

        # we're assessing every race, every player, every racetype
        races = Race.objects.all()
        for race in races:
            results = Results.objects.filter(race=race)

            quali_results_available = results.exclude(position_quali=0).exists()
            sprint_results_available = results.exclude(position_sprint=0).exists()
            race_results_available = results.exclude(position=0).exists()

            # assess all racetypes for each player
            if quali_results_available:
                assess_bets_quali(results=results, race=race)
                quali_ass_status, _ = EventAssessmentStatus.objects.get_or_create(
                    race=race, race_type="quali"
                )
                quali_ass_status.was_assessed = True
                quali_ass_status.save()
            if race.is_sprint and sprint_results_available:
                assess_bets_sprint(results=results, race=race)
                sprint_ass_status, _ = EventAssessmentStatus.objects.get_or_create(
                    race=race, race_type="sprint"
                )
                sprint_ass_status.was_assessed = True
                sprint_ass_status.save()
            if race_results_available:
                assess_bets_race(results=results, race=race)
                race_ass_status, _ = EventAssessmentStatus.objects.get_or_create(
                    race=race, race_type="race"
                )
                race_ass_status.was_assessed = True
                race_ass_status.save()
