from rest_framework import serializers

from base.models import Game, Match, Outcome, Score

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
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