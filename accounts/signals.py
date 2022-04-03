"""
Signals to create and update PlayerProfile records based
on their associated Player records.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Player, PlayerProfile

@receiver(post_save, sender=Player)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a PlayerProfile record when a new Player is created.
    """
    if created:
        PlayerProfile.objects.create(player=instance)

@receiver(post_save, sender=Player)
def update_profile(sender, instance, created, **kwargs):
    """
    Update a PlayerProfile record when its associated
    Player instance is updated.
    """
    if created is False:
        instance.playerprofile.save()
