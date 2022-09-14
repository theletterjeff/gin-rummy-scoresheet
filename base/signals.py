"""
Signals to update Game and Match records.
"""
from django.db.models import Q
from django.db.models.signals import pre_delete, post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from accounts.models import Player
from base.models import Game, Match, Outcome, Score


@receiver(m2m_changed, sender=Match.players.through)
def create_score(sender, **kwargs):
    """
    When a Match is created, create an associated Score.
    """
    if kwargs['action'] == 'post_add':
        for player_pk in kwargs['pk_set']:
            try:
                Score.objects.get(Q(player__pk=player_pk),
                                  Q(match__pk=kwargs['instance'].pk))
            except Score.DoesNotExist:
                Score.objects.create(match=kwargs['instance'],
                                     player=Player.objects.get(pk=player_pk),
                                     player_score=0)

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
    # Set conditions for when we activate this signal
    target_score_gte = (instance.player_score >= instance.match.target_score)
    
    try:
        outcome = Outcome.objects.get(
            match=instance.match, player=instance.player)
    except Outcome.DoesNotExist:
        outcome = None

    if target_score_gte and not outcome:
        
        # Get winner and loser
        winner = instance.player
        
        loser_queryset = instance.match.players.exclude(
            username=winner.username)
        loser = loser_queryset[0]
        
        # Set `complete` and `datetime_ended` attrs
        match = instance.match
        match.complete = True
        match.datetime_ended = timezone.now()
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

@receiver(pre_delete, sender=Game)
def delete_game(sender, instance, **kwargs):
    """
    When Game is deleted, remove its points from the associated Score objects.
    If deleted points put the associated Match below its target_score,
    change Match.complete to False and delete the associated Outcome objects.
    """
    # Remove points from Score
    winner_score = Score.objects.get(
        match=instance.match, player=instance.winner)
    
    winner_score.player_score -= instance.points
    winner_score.save()
    
    if instance.match.complete:
        instance.match.complete = False
        instance.match.datetime_ended = None
        instance.match.save()
        
        Outcome.objects.filter(match=instance.match).delete()