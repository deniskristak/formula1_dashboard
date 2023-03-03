from django.core.management.base import BaseCommand, CommandError
from bets_input.models import Player, RaceBet, Race, Driver, Team


class Command(BaseCommand):
    help = 'Removes all application-defined database data. Use carefully.'

    def handle(self, *args, **options):
        Player.objects.all().delete()
        Race.objects.all().delete()
        RaceBet.objects.all().delete()
        Driver.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed all app data from database'))
