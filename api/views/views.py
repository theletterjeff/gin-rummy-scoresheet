from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)

from api.views.mixins import (AuthenticationMixin, MatchMixin,
                              GameMixin, PlayerMixin)

class AllMatches(MatchMixin, AuthenticationMixin, ListAPIView):
    """
    Return all Match instances.
    """
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AllGames(GameMixin, AuthenticationMixin, ListAPIView):
    """
    Return all Game instances.
    """
    pass

class AllPlayers(PlayerMixin, AuthenticationMixin, ListAPIView):
    """
    Return all Player instances.
    """
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

class CreateMatch(MatchMixin, AuthenticationMixin, CreateAPIView):
    """
    Create a new Match. This view does not add Players to the Match.
    """
    pass

class CreateGame(GameMixin, AuthenticationMixin, CreateAPIView):
    """
    Create a new Game.
    """
    pass
