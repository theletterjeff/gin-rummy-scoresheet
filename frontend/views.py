from django.shortcuts import render

def home(request):
    return render(request, 'frontend/home.html')

def player_list(request):
    raise NotImplementedError

def player_detail(request):
    return render(request, 'frontend/player-profile.html')

def player_edit(request):
    return render(request, 'frontend/player-edit.html')

def match_list(request):
    return render(request, 'frontend/matches.html')

def match_detail(request):
    return render(request, 'frontend/match.html')

def game_detail(request):
    return render(request, 'frontend.game-detail.html')

def game_edit(request):
    return render(request, 'frontend/game-edit.html')