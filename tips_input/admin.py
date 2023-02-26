from django.contrib import admin

from .models import Race, RaceTip, Player, Driver, Team

admin.site.register(Race)
admin.site.register(RaceTip)
admin.site.register(Player)
admin.site.register(Driver)
admin.site.register(Team)
