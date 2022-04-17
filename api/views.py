from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from base.models import Game, Match, Outcome, Score
from .serializers import (GameSerializer, MatchSerializer,
                          OutcomeSerializer, ScoreSerializer)

@api_view(['GET'])
def getAllMatches(request, format=None):
    """
    Return all Match instances.
    """
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getAllGames(request, format=None):
    """
    Return all Game instances.
    """
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)

    return Response(serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
def matchDetail(request, pk, format=None):
    """
    Return, update, or delete a specific Match object.
    """
    try:
        match = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchSerializer(match)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = MatchSerializer(match, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getGame(request, pk, format=None):
    """
    Return a speciic Game object.
    """
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GameSerializer(game, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def createMatch(request, format=None):
    """
    Create a new Match. This view does not add Players to the Match.
    """
    serializer = MatchSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createGame(request, format=None):
    """
    Create a new Game.
    """
    serializer = GameSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
