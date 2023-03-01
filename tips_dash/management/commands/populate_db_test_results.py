from django.core.management.base import BaseCommand, CommandError

# import any model you need:
from tips_input.models import Player, RaceTip, Race, Driver, Team
from tips_dash.models import Results, PlayerPoints
from .test_results.test_data import test_results


class Command(BaseCommand):
    def handle(self, *args, **options):
        Results.objects.all().delete()
        print('Deleted all current test results')

        for test_result_of_race in test_results:
            race = Race.objects.get(id=test_results.index(test_result_of_race)+1)
            for driver in test_result_of_race:
                res = Results(
                    race=race,
                    driver=Driver.objects.get(name=driver),
                    position=test_result_of_race.index(driver)+1,
                    fastest_lap=False if (test_result_of_race.index(driver)+1) != 1 else True,
                    dotd = False if (test_result_of_race.index(driver) + 1) != 2 else True,
                    dnf = False if (test_result_of_race.index(driver) + 1) != len(test_result_of_race)-2 else True,
                )
                res.save()
        print('Inserted new test results')
