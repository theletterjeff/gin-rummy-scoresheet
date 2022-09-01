from django.shortcuts import render

def home(request):
    return render(request, 'frontend/home.html')

def player_detail(request, username):
    return render(request, 'frontend/player-profile.html')

def player_edit(request, username):
    return render(request, 'frontend/player-edit.html')

def match_list(request, username):
    return render(request, 'frontend/matches.html')

def match_detail(request, username, match_pk):
    return render(request, 'frontend/match.html')

def game_detail(request, username, match_pk, game_pk)

def game_edit(request, username, match_pk, game_pk):
    return render(request, 'frontend/game-edit.html')
