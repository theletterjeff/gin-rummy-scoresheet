from config.django.base import *

ALLOWED_HOSTS = ['127.0.0.1']
INSTALLED_APPS += [
    "whitenoise.runserver_nostatic",
]