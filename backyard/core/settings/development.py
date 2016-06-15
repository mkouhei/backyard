"""backyard.core.settings.development."""
from backyard.core.settings.base import *  # noqa


SECRET_KEY = 'rewrite me!'
DEBUG = True
ALLOWED_HOSTS = ['localhost']

ENVIRONMENT = os.path.basename(__file__).split('.py')[0]

INSTALLED_APPS += (
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}

DEBUG_APPS = ''
try:
    from backyard.core.settings.local_settings import *  # noqa
    INSTALLED_APPS += DEBUG_APPS
except ImportError:
    pass
