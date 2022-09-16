from typing import Callable

from django.core.handlers.wsgi import WSGIRequest
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound,
                         HttpResponseNotAllowed, HttpResponseGone,
                         HttpResponseServerError)
from django.urls import reverse
import requests

from api import views


class ApiStatusCheck:
    
    # Status codes mapped to HtppResponse objects
    status_code_resp_dict = {
        400: HttpResponseBadRequest(),
        403: HttpResponseForbidden(),
        404: HttpResponseNotFound(),
        410: HttpResponseGone(),
        500: HttpResponseServerError(),
    }

    # API view names mapped to views
    view_dict = {
        'api:player-detail': views.PlayerDetail,
        'api:player-list-all': views.PlayerListAll,
        'api:player-create': views.PlayerCreate,
        'api:request-player': views.RequestPlayer,

        'api:match-list-player': views.MatchListPlayer,
        'api:game-list-player': views.GameListPlayer,
        'api:score-list-player': views.ScoreListPlayer,
        'api:outcome-list-player': views.OutcomeListPlayer,

        'api:match-detail': views.MatchDetail,
        'api:match-create': views.MatchCreate,
        
        'api:player-list-match': views.PlayerListMatch,
        'api:game-list-match': views.GameListMatch,
        'api:score-list-match': views.ScoreListMatch,
        'api:outcome-list-match': views.OutcomeListMatch,

        'api:score-detail': views.ScoreDetail,
        'api:outcome-detail': views.OutcomeDetail,
    }

    def __init__(
            self, request: WSGIRequest, view_name: str,
            url_kwargs: dict) -> None:
        self.request = request
        self.view_name = view_name
        self.url_kwargs = url_kwargs
    
    def get_api_view_callable(self) -> Callable:
        """Return an API view class as a callable view function."""
        return self.view_dict[self.view_name].as_view()
    
    def get_api_request_status_code(self) -> int:
        view = self.get_api_view_callable()
        return view(self.request, **self.url_kwargs).status_code

    def get_failed_http_response(self, status_code: int) -> HttpResponse:
        try:
            return self.status_code_resp_dict[status_code]
        except KeyError:
            return HttpResponseBadRequest(f'Returned status code {status_code}')
