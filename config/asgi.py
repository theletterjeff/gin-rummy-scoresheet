"""
ASGI config for gin_rummy_scoresheet project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')

application = get_asgi_application()
