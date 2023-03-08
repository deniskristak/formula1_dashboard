from django.db import models

# importing basic models from the input application as we can reuse them for displaying data + creating new models
from bets_input.models import Player, Driver, Race, RaceType


class Results(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(default=0)
    position_quali = models.PositiveSmallIntegerField(default=0)
    position_sprint = models.PositiveSmallIntegerField(default=0)
    fastest_lap = models.BooleanField(default=False)
    dotd = models.BooleanField(default=False)
    dnf = models.BooleanField(default=False)
    dnf_sprint = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.race} - {self.driver} - {self.position}"


class PlayerPoint(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points_race = models.IntegerField(default=0)
    points_sprint = models.IntegerField(default=0)
    points_quali = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.race} - {self.player} - points_race: {self.points_race} - points_sprint: {self.points_sprint} - points_quali: {self.points_quali}"


class PlayerPointsTotal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player} - {self.points_total}"


class EventAssessmentStatus(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    race_type = models.CharField(
        max_length=10,
        choices=RaceType.choices,
    )
    was_assessed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.race} - {self.race_type} Assessed: {self.was_assessed}"
