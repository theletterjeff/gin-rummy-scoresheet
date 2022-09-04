from typing import Tuple

from rest_framework import serializers

class ParameterizedHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """Class to use for `url` fields on Serializers whose URLS draw on 
    attributes from RelatedField instances.
    """
    def __init__(self, lookup_field_data: Tuple[Tuple[str, str, str]],
                 view_name: str = None, **kwargs):
        self.lookup_field_data = lookup_field_data
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None
        
        kwargs = {}

        for related_field_name, lookup_field, lookup_url_kwarg in self.lookup_field_data:

            # Set object to search for attribute in (either self or related field)
            if related_field_name and hasattr(obj, related_field_name):
                target_obj = getattr(obj, related_field_name)
            else:
                target_obj = obj

            lookup_value = getattr(target_obj, lookup_field)
            kwargs.update({lookup_url_kwarg: lookup_value})
        
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
