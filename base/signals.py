"""
Signals to update Game and Match records.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Game, Match, Outcome, Score

@receiver(post_save, sender=Match)
def create_score(sender, instance, created, **kwargs):
    """
    When a Match is created, create an associated Score.
    """
    for player in instance.players.all():
        if len(Score.objects.filter(match=instance, player=player)) == 0:
            Score.objects.create(match=instance, player=player)

@receiver(post_save, sender=Game)
def update_score(sender, instance, created, **kwargs):
    """
    When a Game is entered, Score records are updated.
    """
    if created:
        winner_score = Score.objects.get(
            player=instance.winner,
            match=instance.match
        )
        winner_score.player_score += instance.points
        winner_score.save()

@receiver(pre_save, sender=Score)
def finish_match(sender, instance, **kwargs):
    """
    Whenever a Score is updated, check to see if it exceeds Match.target_score.
    If it does, set the winner and loser on the Outcome records and set
    Match.complete to True.
    """
    if instance.player_score >= instance.match.target_score:
        
        # Get winner and loser
        winner = instance.player
        
        loser_queryset = instance.match.players.exclude(
            username=winner.username)
        loser = loser_queryset[0]
        
        # Set match as complete
        match = instance.match
        match.complete = True
        match.save()
        
        # Set winner's outcome as WIN (1)
        Outcome.objects.create(
            match=instance.match,
            player=winner,
            player_outcome=1
        )

        # Set loser's outcome as LOSE (0)
        Outcome.objects.create(
            match=instance.match,
            player=loser,
            player_outcome=0
        )