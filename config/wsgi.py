"""
WSGI config for gin_rummy_scoresheet project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')

application = WhiteNoise(get_wsgi_application())
