from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_gt_zero(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s must be greater than 0'),
            params={'value': value},
        )