from django.db import models

from .match import Match
from accounts.models import Player
from base.validators import validate_gt_zero

class Game(models.Model):
    """
    A series of games make up one match.
    """
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='games'
    )
    winner = models.ForeignKey(
        Player,
        null=True,
        on_delete=models.SET_NULL,
        related_name='game_wins',
    )
    loser = models.ForeignKey(
        Player,
        null=True,
        on_delete=models.SET_NULL,
        related_name='game_losses',
    )
    points = models.IntegerField(validators=[validate_gt_zero])

    gin = models.BooleanField(default=False)
    undercut = models.BooleanField(default=False)

    datetime_played = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        Player,
        related_name='created_games',
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        datetime_played_str = self.datetime_played.strftime('%D %H:%M')
        match_datetime_started_str = self.match.datetime_started.strftime('%D')
        
        return (
            f'{datetime_played_str} (Match {match_datetime_started_str}) '
            f'({self.pk})'
        )