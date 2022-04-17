from api.serializers import GameSerializer, MatchSerializer
from base.models import Game, Match

class MatchMixin:
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class GameMixin:
    queryset = Game.objects.all()
    serializer_class = GameSerializer