from rest_framework import serializers

from accounts.models import Player
from base.models import Game, Match, Outcome, Score
from base.models.match import MatchPlayer

class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model (auth user model).
    """
    # Reverse relationship
    created_match_set = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Match.objects.all(),
    )
    match_set = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Match.objects.all(),
    )

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):

    players = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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