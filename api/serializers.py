from rest_framework import serializers

from accounts.models import Player
from api.fields import ParameterizedHyperlinkedIdentityField
from base.models import Game, Match, Outcome, Score

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Player model (auth user model).
    """
    url = serializers.HyperlinkedIdentityField(
        lookup_field='username',
        view_name='player-detail',
    )
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
    url = serializers.HyperlinkedIdentityField(
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
        view_name='match-detail',
    )
    players = serializers.HyperlinkedRelatedField(
        view_name='player-detail',
        queryset=Player.objects.all(),
        many=True,
        lookup_field='username',
    )
    games = serializers.HyperlinkedRelatedField(
        view_name='game-detail',
        many=True,
        read_only=True,
    )
    score_set = ParameterizedHyperlinkedIdentityField(
        view_name='score-detail',
        lookup_field_data = (
            ('player', 'username', 'username'),
            ('match', 'pk', 'match_pk'),
        ),
        many=True,
        read_only=True,
    )
    outcome_set = ParameterizedHyperlinkedIdentityField(
        view_name='outcome-detail',
        lookup_field_data = (
            ('player', 'username', 'username'),
            ('match', 'pk', 'match_pk'),
        ),
        many=True,
        read_only=True,
    )
    class Meta:
        model = Match
        fields = '__all__'

class OutcomeSerializer(serializers.HyperlinkedModelSerializer):

    url = ParameterizedHyperlinkedIdentityField(
        view_name='outcome-detail',
        lookup_field_data = (
            ('player', 'username', 'username'),
            ('match', 'pk', 'match_pk'),
        )
    )
    match = serializers.HyperlinkedRelatedField(
        view_name='match-detail',
        queryset=Match.objects.all(),
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
    )
    player = serializers.HyperlinkedRelatedField(
        view_name='player-detail',
        queryset=Player.objects.all(),
        lookup_field='username',
    )
    class Meta:
        model = Outcome
        fields = '__all__'

class ScoreSerializer(serializers.HyperlinkedModelSerializer):

    url = ParameterizedHyperlinkedIdentityField(
        view_name='score-detail',
        lookup_field_data = (
            ('player', 'username', 'username'),
            ('match', 'pk', 'match_pk'),
        )
    )
    match = serializers.HyperlinkedRelatedField(
        view_name='match-detail',
        queryset=Match.objects.all(),
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
    )
    player = serializers.HyperlinkedRelatedField(
        view_name='player-detail',
        queryset=Player.objects.all(),
        lookup_field='username',
    )
    class Meta:
        model = Score
        fields = '__all__'
