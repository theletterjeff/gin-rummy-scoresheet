from django.db import models

from accounts.models import Player
from base.validators import validate_gt_zero

class Match(models.Model):
    """
    A Match consists of multiple Game objects. 
    It concludes when one player's score reaches 500.
    """
    players = models.ManyToManyField(Player, related_name='matches')
    datetime_started = models.DateTimeField(auto_now_add=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)

    target_score = models.IntegerField(
        default=500,
        validators=[validate_gt_zero],
    )
    complete=models.BooleanField(default=False)

class MatchPlayer(models.Model):
    """
    An abstract base class for individual Players and each of their Matches.
    """
    match = models.ForeignKey(Match, null=True, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract=True
        unique_together=('match', 'player')

class Score(MatchPlayer):
    """
    The score for each player in a match.
    """
    player_score = models.IntegerField(default=0)

class Outcome(MatchPlayer):
    """
    Wins and losses by Player for each Match.
    """
    WIN = 1
    LOSS = 0
    OUTCOME_CHOICES = (
        (WIN, 'Win'),
        (LOSS, 'Loss'),
    )

    player_outcome = models.IntegerField(
        choices=OUTCOME_CHOICES,
        null=True,
        blank=True,
    )
    


