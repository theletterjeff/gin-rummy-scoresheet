from django.shortcuts import render

def match(request, match_id):
    return render(request, 'frontend/match.html')

def login(request):
    return render(request, 'registration/login.html')

def home(request):
    return render(request, 'frontend/home.html')