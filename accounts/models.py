from django.contrib.auth.models import AbstractUser
from django.db import models

class Player(AbstractUser):
    """
    The auth_user_model.
    """
    pass

    def __str__(self):
        return self.username