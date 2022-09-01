import re

from django.middleware.csrf import get_token

from accounts.models import Player

def get_value_from_url(pattern: re.Pattern, url: str):
    """Given a re.Pattern, return the matched substring from a URL string."""
    matched_strings = pattern.findall(url)
    if len(matched_strings) > 1:
        raise Exception('More than one match returned from URL.')
    return matched_strings[0]

def get_pk_from_match_url(url: str):
    """Get the `pk` kwarg from a Match URL following the URL pattern:
    'match/<str:pk>/'
    """
    pattern = re.compile(r'\d+(?=\/$)')
    return get_value_from_url(pattern, url)
