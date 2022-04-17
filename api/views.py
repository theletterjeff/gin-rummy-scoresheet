from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import (GenericAPIView,
                                     CreateAPIView,
                                     ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin)

from base.models import Game, Match, Outcome, Score
from .serializers import (GameSerializer, MatchSerializer,
                          OutcomeSerializer, ScoreSerializer)

class AllMatches(ListAPIView):
    """
    Return all Match instances.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class AllGames(ListAPIView):
    """
    Return all Game instances.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class MatchDetail(RetrieveUpdateDestroyAPIView):
    """
    Return, update, or delete a specific Match object.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class GameDetail(RetrieveUpdateDestroyAPIView):
    """
    Return a speciic Game object.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class CreateMatch(CreateAPIView):
    """
    Create a new Match. This view does not add Players to the Match.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class CreateGame(CreateAPIView):
    """
    Create a new Game.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
