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