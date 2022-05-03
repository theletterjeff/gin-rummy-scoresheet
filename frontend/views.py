from django.shortcuts import render

def match(request, match_id):
    return render(request, 'frontend/match.html')