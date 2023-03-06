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
    points = models.IntegerField()

    def __str__(self):
        return f"{self.race} - {self.player} - {self.points}"
