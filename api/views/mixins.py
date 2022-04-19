from rest_framework.permissions import IsAuthenticatedOrReadOnly

from accounts.models import Player
from api.permissions import IsOwnerOrReadyOnly
from api.serializers import GameSerializer, MatchSerializer, PlayerSerializer
from base.models import Game, Match

class AuthenticationMixin:
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadyOnly,
    ]

class MatchMixin:
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class GameMixin:
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PlayerMixin:
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer