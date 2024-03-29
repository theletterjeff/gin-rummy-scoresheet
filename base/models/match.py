from django.db import models
from django.urls import reverse

from accounts.models import Player
from base.validators import validate_gt_zero

class Match(models.Model):
    """
    A Match consists of multiple Game objects. 
    It concludes when one player's score reaches 500.
    """
    players = models.ManyToManyField(Player, related_name='match_set')

    datetime_started = models.DateTimeField(auto_now_add=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)

    target_score = models.IntegerField(
        default=500,
        validators=[validate_gt_zero],
    )
    complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-datetime_started']

    def __str__(self):
        date_started_str = self.datetime_started.strftime('%D')
        return f'{date_started_str} ({self.pk})'
    
    def get_absolute_url(self):
        return reverse('api:match-detail', kwargs={'match_pk': self.pk})

class MatchPlayer(models.Model):
    """
    An abstract base class for individual Players and each of their Matches.
    """
    match = models.ForeignKey(Match, null=True, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL)

    def get_url_kwargs(self):
        return {'username': self.player.username, 'match_pk': self.match.pk}

    class Meta:
        abstract = True
        unique_together = ('match', 'player')
        ordering = ['match']

class Score(MatchPlayer):
    """
    The score for each player in a match.
    """
    player_score = models.IntegerField(default=0)

    def __str__(self):
        date_started_str = self.match.datetime_started.strftime('%D')
        return f'{self.player.username} {date_started_str} - {self.player_score} ({self.pk})'
    
    def get_absolute_url(self):
        return reverse('api:score-detail', kwargs=self.get_url_kwargs())

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

    def __str__(self):
        date_started_str = self.match.datetime_started.strftime('%D')
        return f'{self.player.username} {date_started_str} ({self.pk})'

    def get_absolute_url(self):
        return reverse('api:outcome-detail', kwargs=self.get_url_kwargs())
