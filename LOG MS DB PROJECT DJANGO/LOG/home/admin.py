from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    House, Player, Match, MatchHouse, Game, Venue, Ranking, 
    PlayerStatistic, MatchStatistic, MatchResult, GameRule, MatchSchedule, Team
)

# Register each model to appear in the admin interface
admin.site.register(House)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(MatchHouse)
admin.site.register(Game)
admin.site.register(Venue)
admin.site.register(Ranking)
admin.site.register(PlayerStatistic)
admin.site.register(MatchStatistic)
admin.site.register(MatchResult)
admin.site.register(GameRule)
admin.site.register(MatchSchedule)

