from django.db import models

# importing basic models from the input application as we can reuse them for displaying data + creating new models
from bets_input.models import Player, Driver, Race


class Results(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    position_quali = models.PositiveSmallIntegerField()
    position_sprint = models.PositiveSmallIntegerField()
    fastest_lap = models.BooleanField(default=False)
    dotd = models.BooleanField(default=False)
    dnf = models.BooleanField(default=False)
    dnf_sprint = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.race} - {self.driver} - {self.position}"


class PlayerPoints(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points_race = models.IntegerField()
    points_sprint = models.IntegerField()
    points_quali = models.IntegerField()

    def __str__(self):
        return f"{self.race} - {self.player} - points_race: {self.points_race} - points_sprint: {self.points_sprint} - points_quali: {self.points_quali}"


class PlayerPointsTotal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player} - {self.points_total}"
