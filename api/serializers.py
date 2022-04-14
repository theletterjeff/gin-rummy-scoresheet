from rest_framework import serializers

from accounts.models import Player
from base.models import Game, Match, Outcome, Score

class PlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):

    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = '__all__'

class OutcomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Outcome
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Score
        fields = '__all__'