import dj_database_url

from config.django.base import *

ALLOWED_HOSTS = ['gin-rummy-scoresheet.herokuapp.com']
DEBUG = False
INSTALLED_APPS += ["django.contrib.staticfiles"]

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
