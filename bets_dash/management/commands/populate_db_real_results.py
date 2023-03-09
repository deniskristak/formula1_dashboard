from django.core.management.base import BaseCommand

# import any model you need:
from bets_input.models import Race, Driver
from bets_dash.models import Results

from bets_dash.management.commands.real_data.real_data_results import events


class Command(BaseCommand):
    def handle(self, *args, **options):
        Results.objects.all().delete()
        print("Deleted all current GP results")

        for event_count, result_of_race in enumerate(events, start=1):
            if result_of_race.get("weekend_number") != event_count:
                raise KeyError(
                    "Weekend number in data doesn't match the order. Please fix."
                )
            race = Race.objects.get(id=event_count)
            quali_order = result_of_race["quali_order"]
            sprint_order = result_of_race["sprint_order"]
            race_order = result_of_race["race_order"]
            dnfs = result_of_race["dnfs"]
            sprint_dnfs = result_of_race["sprint_dnfs"]
            fastest_lap = result_of_race["fastest_lap"]
            dotd = result_of_race["dotd"]

            for idx in range(0, len(race_order)):
                driver = Driver.objects.get(abbreviation=race_order[idx])
                print(driver)
                try:
                    pos_sprint = sprint_order.index(driver.abbreviation) + 1
                except ValueError:
                    pos_sprint = 0
                Results.objects.create(
                    race=race,
                    driver=driver,
                    position=idx + 1,
                    position_sprint=pos_sprint,
                    position_quali=quali_order.index(driver.abbreviation) + 1,
                    fastest_lap=True if fastest_lap == race_order[idx] else False,
                    dotd=True if dotd == driver.abbreviation else False,
                    dnf=True if dnfs.count(driver.abbreviation) > 0 else False,
                    dnf_sprint=True
                    if sprint_dnfs.count(driver.abbreviation) > 0
                    else False,
                )
        print("Inserted old + new GP results")
