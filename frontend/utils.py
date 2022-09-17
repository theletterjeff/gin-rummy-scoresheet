import functools
from typing import Callable

from django.http import Http404

def check_api_object_exists(model: type, lookup_url_field: str,
                            lookup_model_field: str = None) -> Callable:
    """Decorator to use on frontend views to make sure that the API objects 
    they rely upon exist before loading the page. Return a 404 response and 
    redirect to the 'Not Found' page if they don't.
    """
    def decorate(view_func: Callable) -> Callable:

        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            nonlocal lookup_model_field
            if not lookup_model_field:
                lookup_model_field = lookup_url_field
            lookup_kwarg = {lookup_model_field: kwargs[lookup_url_field]}
            
            try:
                model.objects.get(**lookup_kwarg)
            except model.DoesNotExist:
                raise Http404(f'{model.__name__} object does not exist.')
            
            return view_func(*args, **kwargs)
        return wrapper
    return decorate