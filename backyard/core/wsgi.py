# -*- coding: utf-8 -*-
"""backyard.core.wsgi."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'backyard.core.settings.development')

application = get_wsgi_application()
