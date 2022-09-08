from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def home(request):
    player = request.user
    username = player.username
    redirect_url = reverse('frontend:match-list', kwargs={'username': username})
    return HttpResponseRedirect(redirect_url)

def player_list(request):
    raise NotImplementedError

def player_detail(request, username: str):
    return render(request, 'frontend/player-detail.html')

def player_edit(request, username: str):
    return render(request, 'frontend/player-edit.html')

def match_list(request, username: str):
    return render(request, 'frontend/match-list.html')

def match_detail(request, match_pk: int):
    return render(request, 'frontend/match-detail.html')

def match_edit(request, match_pk: int):
    return render(request, 'frontend/match-edit.html')

def game_detail(request, match_pk: int, game_pk: int):
    return render(request, 'frontend.game-detail.html')

def game_edit(request, match_pk: int, game_pk: int):
    return render(request, 'frontend/game-edit.html')
