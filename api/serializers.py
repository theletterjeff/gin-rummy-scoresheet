from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Player
from base.models import Game, Match, Outcome, Score
from base.models.match import MatchPlayer

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Player model (auth user model).
    """
    match_set = serializers.HyperlinkedRelatedField(
        view_name='match-detail',
        many=True,
        read_only=True,
    )
    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Game
        fields = '__all__'

class MatchSerializer(serializers.HyperlinkedModelSerializer):

    games = serializers.HyperlinkedRelatedField(
        view_name='game-detail',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Match
        fields = '__all__'

class OutcomeSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Outcome
        fields = '__all__'

class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Score
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, player):
        token = super().get_token(player)
        token['username'] = player.username
        return token
