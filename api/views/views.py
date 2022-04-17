from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)

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
