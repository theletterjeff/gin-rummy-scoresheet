from rest_framework.response import Response
from rest_framework.decorators import api_view

from base.models import Game, Match, Outcome, Score
from .serializers import (GameSerializer, MatchSerializer,
                          OutcomeSerializer, ScoreSerializer)

@api_view(['GET'])
def getAllMatches(request):
    """
    Return all Match instances.
    """
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getAllGames(request):
    """
    Return all Game instances.
    """
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getMatch(request, pk):
    """
    Return a specific Match object.
    """
    match = Match.objects.get(pk=pk)
    serializer = MatchSerializer(match, many=False)

    return Response(serializer.data)

@api_view(['GET'])
def getGame(request, pk):
    """
    Return a speciic Game object.
    """
    game = Game.objects.get(pk=pk)
    serializer = GameSerializer(game, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def createMatch(request):
    """
    Create a new Match. This view does not add Players to the Match.
    """
    serializer = MatchSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def createGame(request):
    """
    Create a new Game.
    """
    serializer = GameSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)
