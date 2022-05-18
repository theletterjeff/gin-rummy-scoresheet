from django.shortcuts import render

def match(request, match_id):
    return render(request, 'frontend/match.html')

def game_edit(request, game_id):
    return render(request, 'frontend/game-edit.html')

def home(request):
    return render(request, 'frontend/home.html')

def player(request, player_id):
    return render(request, 'frontend/player.html')