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
        view_name='api:player-detail',
    )
    match_set = serializers.HyperlinkedRelatedField(
        view_name='api:match-detail',
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
        many=True,
        read_only=True,
    )
    class Meta:
        model = Player
        fields = [
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'match_set',
            'last_login',
        ]

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
        view_name='api:match-detail',
    )
    players = serializers.HyperlinkedRelatedField(
        view_name='api:player-detail',
        queryset=Player.objects.all(),
        many=True,
        lookup_field='username',
    )
    games = ParameterizedHyperlinkedIdentityField(
        view_name='api:game-detail',
        lookup_field_data=(
            (None, 'pk', 'match_pk'),
            ('game', 'pk', 'game_pk'),
        ),
        many=True,
        read_only=True,
    )
    score_set = ParameterizedHyperlinkedIdentityField(
        view_name='api:score-detail',
        lookup_field_data = (
            ('player', 'username', 'username'),
            ('match', 'pk', 'match_pk'),
        ),
        many=True,
        read_only=True,
    )
    outcome_set = ParameterizedHyperlinkedIdentityField(
        view_name='api:outcome-detail',
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

class GameSerializer(serializers.HyperlinkedModelSerializer):

    url = ParameterizedHyperlinkedIdentityField(
        view_name='api:game-detail',
        lookup_field_data = (
            ('match', 'pk', 'match_pk'),
            (None, 'pk', 'game_pk'),
        )
    )
    match = serializers.HyperlinkedRelatedField(
        view_name='api:match-detail',
        queryset=Match.objects.all(),
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
    )
    winner = serializers.HyperlinkedRelatedField(
        view_name='api:player-detail',
        queryset=Player.objects.all(),
        lookup_field='username',
    )
    loser = serializers.HyperlinkedRelatedField(
        view_name='api:player-detail',
        queryset=Player.objects.all(),
        lookup_field='username',
    )
    class Meta:
        model = Game
        fields = '__all__'

class OutcomeSerializer(serializers.HyperlinkedModelSerializer):

    url = ParameterizedHyperlinkedIdentityField(
        view_name='api:outcome-detail',
        lookup_field_data = (
            ('player', 'username', 'username'),
            ('match', 'pk', 'match_pk'),
        )
    )
    match = serializers.HyperlinkedRelatedField(
        view_name='api:match-detail',
        queryset=Match.objects.all(),
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
    )
    player = serializers.HyperlinkedRelatedField(
        view_name='api:player-detail',
        queryset=Player.objects.all(),
        lookup_field='username',
    )
    class Meta:
        model = Outcome
        fields = '__all__'

class ScoreSerializer(serializers.HyperlinkedModelSerializer):

    url = ParameterizedHyperlinkedIdentityField(
        view_name='api:score-detail',
        lookup_field_data = (
            ('player', 'username', 'username'),
            ('match', 'pk', 'match_pk'),
        )
    )
    match = serializers.HyperlinkedRelatedField(
        view_name='api:match-detail',
        queryset=Match.objects.all(),
        lookup_field='pk',
        lookup_url_kwarg='match_pk',
    )
    player = serializers.HyperlinkedRelatedField(
        view_name='api:player-detail',
        queryset=Player.objects.all(),
        lookup_field='username',
    )
    class Meta:
        model = Score
        fields = '__all__'
