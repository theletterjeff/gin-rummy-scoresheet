from django.shortcuts import render

def matches(request):
    return render(request, 'frontend/matches.html')

def match(request, match_id):
    return render(request, 'frontend/match.html')

def game_edit(request, game_id):
    return render(request, 'frontend/game-edit.html')

def home(request):
    return render(request, 'frontend/home.html')

def player_profile(request, username):
    return render(request, 'frontend/player-profile.html')

def player_edit(request, player_id):
    return render(request, 'frontend/player-edit.html')