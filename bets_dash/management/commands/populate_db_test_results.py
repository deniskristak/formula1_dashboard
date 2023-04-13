from django.core.management.base import BaseCommand

# import any model you need:
from bets_input.models import Race, Driver
from bets_dash.models import Results
from bets_dash.management.commands.test_data.test_data_results import test_results


class Command(BaseCommand):
    def handle(self, *args, **options):
        Results.objects.all().delete()
        print("Deleted all current test results")

        for tr_count, test_result_of_race in enumerate(test_results, start=1):
            race = Race.objects.get(id=tr_count)
            for count, driver in enumerate(test_result_of_race, start=1):
                res = Results(
                    race=race,
                    driver=Driver.objects.get(name=driver),
                    position=count,
                    position_sprint=count,
                    position_quali=count,
                    fastest_lap=False if count != 1 else True,
                    dotd=False if count != 2 else True,
                    dnf=False if count != len(test_result_of_race) - 2 else True,
                    dnf_sprint=False if count != len(test_result_of_race) - 2 else True,
                )
                res.save()
        print("Inserted new test results")
