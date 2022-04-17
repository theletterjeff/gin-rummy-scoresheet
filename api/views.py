from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import (GenericAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin)

from base.models import Game, Match, Outcome, Score
from .serializers import (GameSerializer, MatchSerializer,
                          OutcomeSerializer, ScoreSerializer)

class AllMatches(GenericAPIView, ListModelMixin):
    """
    Return all Match instances.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AllGames(GenericAPIView, ListModelMixin):
    """
    Return all Game instances.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

class CreateMatch(GenericAPIView, CreateModelMixin):
    """
    Create a new Match. This view does not add Players to the Match.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CreateGame(GenericAPIView, CreateModelMixin):
    """
    Create a new Game.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
