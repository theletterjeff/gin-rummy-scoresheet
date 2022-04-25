from django.shortcuts import render

def home(request):
    return render(request, 'frontend/home.html')

def match(request):
    return render(request, 'frontend/match.html')