from django.core.management.base import BaseCommand, CommandError

# import any model you need:
from tips_input.models import Player, RaceTip, Race, Driver, Team
# from tips_dash.models import

# run with `pyhon manage.py edov_cmd`
class Command(BaseCommand):
    # what displays after `pyhon manage.py edov_cmd --help`
    help = ''

    # in this method, you write what the cmd should do
    def handle(self, *args, **options):

        ##### examples ######

        # look into tips_dash/models.py and tips_input/models.py for more information on what models are available and what fields they have

        # create a new Player and save him to database
        new_player = Player(
            nickname="edoooooo",
            fullname="Eduard Kofira"
        )
        new_player.save()

        # get all instances of RaceTip
        racetips = RaceTip.objects.all()

        # get a single instance of Player
        my_player = Player.objects.get(nickname='tomasko')

        # filter race tips by race and player
        racetips_filtered = RaceTip.objects.filter(
            race=Race.objects.get(
                name="Jeddah Corniche Circuit"
            ),
            player=my_player
        )

        # put filtered racetips into a list with just the driver's name and position
        tips = []
        for tip in racetips_filtered:
            tips.append([
                tip.driver.name,
                tip.position
            ])

        print(tips)
