from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class Player(AbstractUser):
    """
    The auth_user_model.
    """
    class Meta:
        ordering = ['pk']
    
    def get_absolute_url(self):
        return reverse('player-detail', kwargs={'username': self.username})
    
    def __str__(self):
        return self.username

class PlayerProfile(models.Model):
    """
    Profile details for Players.
    """
    player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.username