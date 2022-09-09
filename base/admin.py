from django.contrib import admin

from base.models import Match, Game, Score, Outcome

admin.site.register(Match)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Outcome)