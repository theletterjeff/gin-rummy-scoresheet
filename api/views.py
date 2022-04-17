from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin)

from base.models import Game, Match, Outcome, Score
from .serializers import (GameSerializer, MatchSerializer,
                          OutcomeSerializer, ScoreSerializer)

class AllMatches(GenericAPIView, ListModelMixin):
    """
    Return all Match instances.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AllGames(GenericAPIView, ListModelMixin):
    """
    Return all Game instances.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MatchDetail(APIView):
    """
    Return, update, or delete a specific Match object.
    """
    def get_object(self, pk):
        try:
            return Match.objects.get(pk=pk)
        except Match.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        match = self.get_object(pk)
        serializer = MatchSerializer(match)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        match = self.get_object(pk)
        serializer = MatchSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        match = self.get_object(pk)
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GameDetail(APIView):
    """
    Return a speciic Game object.
    """
    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        game = self.get_object(pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateMatch(APIView):
    """
    Create a new Match. This view does not add Players to the Match.
    """
    def post(self, request, format=None):
        serializer = MatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateGame(APIView):
    """
    Create a new Game.
    """
    def post(self, request, format=None):
        serializer = GameSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
