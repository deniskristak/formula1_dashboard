from django.core.management.base import BaseCommand
from bets_input.models import Player, RaceBet, Race, Driver, Team
from bets_dash.models import Results, PlayerPoints


class Command(BaseCommand):
    help = "Removes all application-defined database data. Use carefully."

    def handle(self, *args, **options):
        answer = input("Are you really sure? Type 'yes'\n")
        if answer != "yes":
            self.stdout.write(self.style.WARNING("You weren't sure."))
        else:
            Player.objects.all().delete()
            Race.objects.all().delete()
            RaceBet.objects.all().delete()
            Driver.objects.all().delete()
            Team.objects.all().delete()
            Results.objects.all().delete()
            PlayerPoints.objects.all().delete()

            self.stdout.write(
                self.style.SUCCESS("Successfully removed all app data from database")
            )
