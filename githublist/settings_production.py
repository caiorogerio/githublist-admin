from .settings import *
import django_heroku

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = False

ALLOWED_HOSTS = [
    'ateliware-case-github-admin.herokuapp.com',
]

# Configure Django App for Heroku.
TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'

django_heroku.settings(locals())

# CORS config
CORS_ORIGIN_WHITELIST = (
    'https://ateliware-case-github.herokuapp.com',
    'http://ateliware-case-github.herokuapp.com',
)

