from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse

from accounts.models import Player
from api.permissions import IsOwnerOrReadOnly, IsRequestUser
from api.serializers import (GameSerializer, MatchSerializer, OutcomeSerializer,
                             PlayerSerializer, ScoreSerializer)
from base.models import Game, Match, Outcome, Score

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'matches': reverse('match-list-create', request=request, format=format),
        'games': reverse('game-list-create', request=request, format=format),
        'players': reverse('player-list', request=request, format=format),
    })

class MatchList(ListCreateAPIView):
    """GET all Matches or POST a new Match. Creating a new Match automatically
    assigns the current request.user to the `created_by` Match field.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class GameList(ListCreateAPIView):
    """GET all Games or POST a new Game. Creating a new Game automatically
    assigns the current request.user to the `created_by` Game field.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PlayerList(ListAPIView):
    """GET all Player instances."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class PlayerCreate(CreateAPIView):
    """POST a new Player"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class MatchDetail(RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, or DELETE a Match."""
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class GameDetail(RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, or DELETE a Game."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class PlayerDetail(RetrieveAPIView):
    """GET a Player object."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class ScoreDetail(RetrieveAPIView):
    """GET a Player's Score for a Match."""
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class PlayerEdit(UpdateAPIView):
    """PUT or PATCH a Player profile.
    To do: figure out correct `permission_classes`.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [
        IsRequestUser,
    ]

class OutcomeDetail(RetrieveAPIView):
    """GET an Outcome instance for a Match."""
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]