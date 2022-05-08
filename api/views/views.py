from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.views.mixins import (AuthenticationMixin, MatchMixin,
                              GameMixin, PlayerMixin)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'matches': reverse('match-list-create', request=request, format=format),
        'games': reverse('game-list-create', request=request, format=format),
        'players': reverse('player-list', request=request, format=format),
    })

class MatchList(MatchMixin, AuthenticationMixin, ListCreateAPIView):
    """
    Return all Match instances.
    """
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class GameList(GameMixin, AuthenticationMixin, ListCreateAPIView):
    """
    Return all Game instances.
    """
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PlayerList(PlayerMixin, AuthenticationMixin, ListAPIView):
    """
    Return all Player instances.
    """
    pass

class PlayerCreate(PlayerMixin, CreateAPIView):
    """Create a new Player"""
    pass

class MatchDetail(MatchMixin, AuthenticationMixin, RetrieveUpdateDestroyAPIView):
    """
    Return, update, or delete a specific Match object.
    """
    pass

class GameDetail(GameMixin, AuthenticationMixin, RetrieveUpdateDestroyAPIView):
    """
    Return a specific Game object.
    """
    pass

class PlayerDetail(PlayerMixin, AuthenticationMixin, RetrieveAPIView):
    """
    Return a specific Player object.
    """
    pass