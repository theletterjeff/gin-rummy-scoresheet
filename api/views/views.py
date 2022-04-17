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

from api.serializers import (GameSerializer, MatchSerializer,
                             OutcomeSerializer, ScoreSerializer)
from base.models import Game, Match, Outcome, Score
from api.views.mixins import MatchMixin, GameMixin

class AllMatches(MatchMixin, ListAPIView):
    """
    Return all Match instances.
    """
    pass

class AllGames(GameMixin, ListAPIView):
    """
    Return all Game instances.
    """
    pass

class MatchDetail(MatchMixin, RetrieveUpdateDestroyAPIView):
    """
    Return, update, or delete a specific Match object.
    """
    pass

class GameDetail(GameMixin, RetrieveUpdateDestroyAPIView):
    """
    Return a speciic Game object.
    """
    pass

class CreateMatch(MatchMixin, CreateAPIView):
    """
    Create a new Match. This view does not add Players to the Match.
    """
    pass

class CreateGame(GameMixin, CreateAPIView):
    """
    Create a new Game.
    """
    pass
