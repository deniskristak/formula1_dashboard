from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=300)
    lc_name = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name}"


class Driver(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=3)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    default_position = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Race(models.Model):
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    is_sprint = models.BooleanField(default=False)
    datetime_of_race_gmt = models.DateTimeField(auto_now=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['datetime_of_race_gmt']


class Player(models.Model):
    fullname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nickname}"


class RaceTip(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    position_sprint = models.PositiveSmallIntegerField()
    position_quali = models.PositiveSmallIntegerField()
    fastest_lap = models.BooleanField(default=False)
    dotd = models.BooleanField(default=False)
    dnf = models.BooleanField(default=False)
    dnf_sprint = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player}-{self.race}-{self.driver} POS: {self.position} SPRINT_POS: {self.position_sprint} QUALI_POS: {self.position_quali}"

    class Meta:
        ordering = ['position']
