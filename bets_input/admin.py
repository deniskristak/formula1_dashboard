from django.contrib import admin

from .models import Race, RaceBet, Player, Driver, Team

admin.site.register(Race)
admin.site.register(RaceBet)
admin.site.register(Player)
admin.site.register(Driver)
admin.site.register(Team)
