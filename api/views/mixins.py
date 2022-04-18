from accounts.models import Player
from api.serializers import GameSerializer, MatchSerializer, PlayerSerializer
from base.models import Game, Match

class MatchMixin:
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class GameMixin:
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PlayerMixin:
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer