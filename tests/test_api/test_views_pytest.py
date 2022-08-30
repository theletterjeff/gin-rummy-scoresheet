from django.urls import reverse

from rest_framework.test import APIRequestFactory, force_authenticate

from api.views import MatchList
from tests.fixtures import player1, player2, simple_match

def test_match_list_for_player(player1, player2, simple_match):
    factory = APIRequestFactory()
    view = MatchList.as_view()

    request = factory.get(reverse('match-list', args=['player1']))
    force_authenticate(request, user=player1)
    response = view(request)
    pass