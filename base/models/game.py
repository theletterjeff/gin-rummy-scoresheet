from django.db import models

from .match import Match
from accounts.models import Player
from base.validators import validate_gt_zero

class Game(models.Model):
    """
    A series of games make up one match.
    """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

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