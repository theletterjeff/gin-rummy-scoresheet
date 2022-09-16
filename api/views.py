from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrObjectPlayer
from api.serializers import (GameSerializer, MatchSerializer, OutcomeSerializer,
                             PlayerSerializer, ScoreSerializer)

from accounts.models import Player
from base.models import Game, Match, Outcome, Score

# Player

class PlayerDetail(RetrieveUpdateDestroyAPIView):
    """GET a Player object."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'username'

class PlayerListAll(ListAPIView):
    """GET all Player instances."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerCreate(CreateAPIView):
    """POST a new Player"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [AllowAny]

class RequestPlayer(APIView):
    """GET serialized data for the currently logged in Player.
    This should solve some of my challenges around accessing the identity
    of the currently logged in Player.
    """
    def get(self, request, format=None):
        player = request.user
        serializer = PlayerSerializer(player,
                                      context={'request': request})
        return Response(serializer.data)


# Lists by Player

class MatchListPlayer(ListAPIView):
    """GET a list of Match objects for the specified user."""
    serializer_class = MatchSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Match.objects.filter(players__username=username)

class GameListPlayer(ListAPIView):
    """GET a list of Game objects for the specified user."""
    serializer_class = GameSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Game.objects.filter(Q(winner__username=username) |
                                    Q(loser__username=username))

class ScoreListPlayer(ListAPIView):
    """GET a list of Score objects for the specified user."""
    serializer_class = ScoreSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Score.objects.filter(player__username=username)

class OutcomeListPlayer(ListAPIView):
    """GET a list of Outcome objects for the specified user."""
    serializer_class = OutcomeSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Outcome.objects.filter(player__username=username)


# Match

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


# Lists by Match

class PlayerListMatch(ListAPIView):
    """GET a Match's list of Players."""
    serializer_class = PlayerSerializer
    def get_queryset(self):
        match_pk = self.kwargs['match_pk']
        match = Match.objects.get(pk=match_pk)
        return Player.objects.filter(match_set=match)

class GameListMatch(ListAPIView):
    """GET a Match's list of Games."""
    serializer_class = GameSerializer
    def get_queryset(self):
        match_pk = self.kwargs['match_pk']
        match = Match.objects.get(pk=match_pk)
        return Game.objects.filter(match=match)

class ScoreListMatch(ListAPIView):
    """GET a Match's list of Scores."""
    serializer_class = ScoreSerializer
    def get_queryset(self):
        match_pk = self.kwargs['match_pk']
        match = Match.objects.get(pk=match_pk)
        return Score.objects.filter(match=match)

class OutcomeListMatch(ListAPIView):
    """GET a Match's list of Outcomes."""
    serializer_class = OutcomeSerializer
    def get_queryset(self):
        match_pk = self.kwargs['match_pk']
        match = Match.objects.get(pk=match_pk)
        return Outcome.objects.filter(match=match)


# Game

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


# Score and Outcome

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
