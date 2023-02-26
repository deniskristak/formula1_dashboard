from django.core.management.base import BaseCommand, CommandError
import os
from tips_input.models import Player, RaceTip, Race, Driver, Team
import csv


class Command(BaseCommand):
    help = 'Populates database with initial data'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))

        list_of_teams = self.read_data("tips_input_team.csv")
        for team in list_of_teams:
            new_team = Team(
                name=team[1]
            )
            new_team.save()

        list_of_drivers = self.read_data("tips_input_driver.csv")
        for driver in list_of_drivers:
            new_driver = Driver(
                name=driver[1],
                default_position=driver[2],
                team=Team.objects.get(pk=driver[3])
            )
            new_driver.save()

        list_of_players = self.read_data("tips_input_player.csv")
        for player in list_of_players:
            new_player = Player(
                fullname=player[1],
                nickname=player[2]
            )
            new_player.save()

        list_of_races = self.read_data("tips_input_race.csv")
        for race in list_of_races:
            new_race = Race(
                name=race[1],
                country=race[2],
                is_sprint=race[3],
                datetime_of_race_gmt=race[4],
            )
            new_race.save()

        all_drivers = Driver.objects.all()
        all_players = Player.objects.all()
        all_races = Race.objects.all()
        for driver in all_drivers:
            for player in all_players:
                for race in all_races:
                    new_racetip = RaceTip(
                        driver=driver,
                        player=player,
                        race=race,
                        position=driver.default_position,
                        position_quali=driver.default_position
                    )
                    new_racetip.save()

    @staticmethod
    def read_data(data_filename):
        here = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(here, "initial_data")

        with open(os.path.join(data_dir, data_filename), 'r') as teams:
            # Return a reader object which will
            # iterate over lines in the given csvfile
            csv_reader = csv.reader(teams)

            # convert string to list
            list_of_items = list(csv_reader)
            return list_of_items
