from django.core.management.base import BaseCommand

# import any model you need:
from bets_input.models import Race, Driver, RaceBet, Player, PlayerPlacedBet
from bets_dash.models import Results

from bets_dash.management.commands.real_data.real_data_bets import bets


class Command(BaseCommand):
    def handle(self, *args, **options):
        for bet in bets:
            player = Player.objects.get(id=bet["player_id"])
            race = Race.objects.get(id=bet["race_id"])
            quali_order = bet["quali_order"]
            sprint_order = bet["sprint_order"]
            race_order = bet["race_order"]
            dnfs = bet["dnfs"]
            sprint_dnfs = bet["sprint_dnfs"]
            fastest_lap = bet["fastest_lap"]
            dotd = bet["dotd"]
            print(player)
            print(race)

            race_order_set = len(race_order) > 1
            sprint_order_set = len(sprint_order) > 1
            quali_order_set = len(quali_order) > 1

            if race_order_set:
                for idx in range(0, len(race_order)):
                    driver = Driver.objects.get(abbreviation=race_order[idx])
                    try:
                        pos_sprint = sprint_order.index(driver.abbreviation) + 1
                    except ValueError:
                        pos_sprint = 0
                    try:
                        pos_quali = quali_order.index(driver.abbreviation) + 1
                    except ValueError:
                        pos_quali = 0

                    rb, _ = RaceBet.objects.get_or_create(
                        race=race,
                        player=player,
                        driver=driver,
                    )
                    rb.position = idx + 1
                    rb.position_sprint = pos_sprint
                    rb.position_quali = pos_quali
                    rb.fastest_lap = fastest_lap = (
                        True if fastest_lap == race_order[idx] else False
                    )
                    rb.dotd = True if dotd == driver.abbreviation else False
                    rb.dnf = True if driver.abbreviation in dnfs else False
                    rb.dnf_sprint = (
                        True if driver.abbreviation in sprint_dnfs else False
                    )
                    rb.save()

            elif sprint_order_set:
                for idx in range(0, len(sprint_order)):
                    driver = Driver.objects.get(abbreviation=sprint_order[idx])
                    # this only runs if race order is [], therefore we set the race position to 0
                    pos_race = 0
                    try:
                        pos_quali = quali_order.index(driver.abbreviation) + 1
                    except ValueError:
                        pos_quali = 0
                    rb, _ = RaceBet.objects.get_or_create(
                        race=race,
                        player=player,
                        driver=driver,
                    )
                    rb.position = pos_race
                    rb.position_sprint = idx + 1
                    rb.position_quali = pos_quali
                    rb.fastest_lap = False
                    rb.dotd = False
                    rb.dnf = False
                    rb.dnf_sprint = (
                        True if driver.abbreviation in sprint_dnfs else False
                    )
                    rb.save()
            elif quali_order_set:
                for idx in range(0, len(quali_order)):
                    driver = Driver.objects.get(abbreviation=quali_order[idx])
                    # this only runs if race_order and sprint_order are [], therefore we set those race positions to 0
                    pos_race = 0
                    pos_sprint = 0

                    rb, _ = RaceBet.objects.get_or_create(
                        race=race,
                        player=player,
                        driver=driver,
                    )
                    rb.position = pos_race
                    rb.position_sprint = pos_sprint
                    rb.position_quali = idx + 1
                    rb.fastest_lap = False
                    rb.dotd = False
                    rb.dnf = False
                    rb.dnf_sprint = False
                    rb.save()

            if race_order_set:
                PlayerPlacedBet.objects.get_or_create(
                    player=player, race=race, race_type="race"
                )
            if sprint_order_set:
                PlayerPlacedBet.objects.get_or_create(
                    player=player, race=race, race_type="sprint"
                )
            if quali_order_set:
                PlayerPlacedBet.objects.get_or_create(
                    player=player, race=race, race_type="quali"
                )
        print("Inserted new bets")
