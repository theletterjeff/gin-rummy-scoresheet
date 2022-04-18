from rest_framework.generics import (CreateAPIView, ListAPIView, 
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)

from api.views.mixins import MatchMixin, GameMixin, PlayerMixin

class AllMatches(MatchMixin, ListAPIView):
    """
    Return all Match instances.
    """
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AllGames(GameMixin, ListAPIView):
    """
    Return all Game instances.
    """
    pass

class AllPlayers(PlayerMixin, ListAPIView):
    """
    Return all Player instances.
    """
    pass

class MatchDetail(MatchMixin, RetrieveUpdateDestroyAPIView):
    """
    Return, update, or delete a specific Match object.
    """
    pass

class GameDetail(GameMixin, RetrieveUpdateDestroyAPIView):
    """
    Return a specific Game object.
    """
    pass

class PlayerDetail(PlayerMixin, RetrieveAPIView):
    """
    Return a specific Player object.
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
