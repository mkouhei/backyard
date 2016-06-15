"""backyard.core.settings.testing."""
from backyard.core.settings.base import *  # noqa

SECRET_KEY = 'rewrite me!'
DEBUG = True
ALLOWED_HOSTS = []

ENVIRONMENT = os.path.basename(__file__).split('.py')[0]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
    }
}
