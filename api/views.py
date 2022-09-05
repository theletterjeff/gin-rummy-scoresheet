from django.shortcuts import get_object_or_404

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

class GameList(ListAPIView):
    """GET all Games or POST a new Game."""
    serializer_class = GameSerializer
    def get_queryset(self):
        match_pk = self.kwargs['match_pk']
        match = Match.objects.get(pk=match_pk)
        return Game.objects.filter(match=match)

class GameDetail(RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, or DELETE a Game."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,
                                match__pk=self.kwargs['match_pk'],
                                pk=self.kwargs['game_pk'])
        self.check_object_permissions(self.request, obj)
        return obj

class GameCreate(CreateAPIView):
    """POST a Game."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class ScoreList(ListAPIView):
    serializer_class = ScoreSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        player = Player.objects.get(username=username)
        return Score.objects.filter(player=player)

class ScoreDetail(RetrieveAPIView):
    """GET a Player's Score for a Match."""
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,
                                player__username=self.kwargs['username'],
                                match__pk=self.kwargs['match_pk'])
        self.check_object_permissions(self.request, obj)
        return obj

class OutcomeList(ListAPIView):
    """GET all Outcome instances for a Player."""
    serializer_class = OutcomeSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        player = Player.objects.get(username=username)
        return Outcome.objects.filter(player=player)

class OutcomeDetail(RetrieveAPIView):
    """GET an Outcome instance for a Match."""
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,
                                player__username=self.kwargs['username'],
                                match__pk=self.kwargs['match_pk'])
        self.check_object_permissions(self.request, obj)
        return obj
        


class PlayerList(ListAPIView):
    """GET all Player instances."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerCreate(CreateAPIView):
    """POST a new Player"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(RetrieveUpdateDestroyAPIView):
    """GET a Player object."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field='username'

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
