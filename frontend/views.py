from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from accounts.models import Player
from base.models import Match, Game, Score, Outcome
from frontend.utils import check_api_object_exists, fallback_403

def home(request):
    return render(request, 'frontend/home.html')

@login_required
def player_list_all(request):
    return render(request, 'frontend/player-list-all.html')

@login_required
@check_api_object_exists(Player, 'username')
def player_detail(request, username: str):
    return render(request, 'frontend/player-detail.html')

@login_required
@check_api_object_exists(Player, 'username')
def player_edit(request, username: str):
    if request.user.username != username:
        return fallback_403(request)
    return render(request, 'frontend/player-edit.html')

@login_required
@check_api_object_exists(Player, 'username')
def match_list(request, username: str):
    return render(request, 'frontend/match-list.html')

@login_required
@check_api_object_exists(Match, 'match_pk', 'pk')
def match_detail(request, match_pk: int):
    return render(request, 'frontend/match-detail.html')

@login_required
@check_api_object_exists(Match, 'match_pk', 'pk')
def match_edit(request, match_pk: int):
    raise NotImplementedError

@login_required
@check_api_object_exists(Game, 'game_pk', 'pk')
def game_detail(request, match_pk: int, game_pk: int):
    raise NotImplementedError()

@login_required
@check_api_object_exists(Game, 'game_pk', 'pk')
def game_edit(request, match_pk: int, game_pk: int):
    return render(request, 'frontend/game-edit.html')
