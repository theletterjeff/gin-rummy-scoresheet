from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import Player
from base.models import Match, Game, Score, Outcome 

class IsAuthenticatedOrObjectPlayer(BasePermission):
    """Custom permission for handling views derived from the generic 
    RetrieveUpdateDestroy class. Authenticated users can use GET requests, 
    users who are the object player can access PATCH, PUT, and DELETE.
    """
    def has_object_permission(self, request, view, obj):
        is_auth = bool(request.user and request.user.is_authenticated)
        is_safe_method = bool(request.method in SAFE_METHODS)
        is_obj_player = bool(self.check_request_user_in_obj(request, obj))

        if (is_auth and is_safe_method) or (is_obj_player):
            return True
        return False

    def check_request_user_in_obj(self, request, obj):
        model_funcs = {
            Match: self._check_request_user_in_match_players,
            Game: self._check_request_user_in_game_players,
            Score: self._check_request_user_in_score_outcome,
            Outcome: self._check_request_user_in_score_outcome,
            Player: self._check_request_user_is_player,
        }
        return model_funcs[type(obj)](request, obj)

    def _check_request_user_in_match_players(self, request, match_obj):
        return request.user in match_obj.players.all()
    
    def _check_request_user_in_game_players(self, request, game_obj):
        return request.user == game_obj.winner or request.user == game_obj.loser
    
    def _check_request_user_in_score_outcome(self, request, score_outcome_obj):
        return request.user == score_outcome_obj.player

    def _check_request_user_is_player(self, request, player_obj):
        return request.user == player_obj