from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api.permissions import IsRequestUser
from api.serializers import (GameSerializer, MatchSerializer, OutcomeSerializer,
                             PlayerSerializer, ScoreSerializer)

from accounts.models import Player
from base.models import Game, Match, Outcome, Score

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'matches': reverse('match-list', request=request, format=format),
        'games': reverse('game-list-create', request=request, format=format),
        'players': reverse('player-list', request=request, format=format),
        'player-matches': reverse('player-matches', request=request, format=format),
    })

class MatchList(ListAPIView):
    """GET a list of Match objects for the specified user."""
    serializer_class = MatchSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Match.objects.filter(players__username=username)

class MatchDetail(RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, or DELETE a Match."""
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_url_kwarg = 'match_pk'
    lookup_field = 'pk'

class MatchCreate(CreateAPIView):
    """POST a Match."""
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class GameList(ListCreateAPIView):
    """GET all Games or POST a new Game."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PlayerList(ListAPIView):
    """GET all Player instances."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerCreate(CreateAPIView):
    """POST a new Player"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class GameDetail(RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, or DELETE a Game."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PlayerDetail(RetrieveUpdateDestroyAPIView):
    """GET a Player object."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field='username'

class ScoreDetail(RetrieveAPIView):
    """GET a Player's Score for a Match."""
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class OutcomeDetail(RetrieveAPIView):
    """GET an Outcome instance for a Match."""
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer

class PlayerMatches(APIView):
    """GET Match instances played by a Player."""
    def get(self, request, format=None):
        player_matches = Match.objects.filter(players__in=str(request.user.pk))
        serializer = MatchSerializer(player_matches,
                                     context={'request': request},
                                     many=True)
        return Response(serializer.data)

class LoggedInPlayerDetail(APIView):
    """GET serialized data for the currently logged in Player.
    This should solve some of my challenges around accessing the identity
    of the currently logged in Player.
    """
    def get(self, request, format=None):
        player = request.user
        serializer = PlayerSerializer(player,
                                      context={'request': request})
        return Response(serializer.data)
