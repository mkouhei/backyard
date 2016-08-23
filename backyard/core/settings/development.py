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

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

DEBUG_APPS = ''
try:
    from backyard.core.settings.local_settings import *  # noqa
    INSTALLED_APPS += DEBUG_APPS
except ImportError:
    pass
