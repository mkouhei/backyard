# -*- coding: utf-8 -*-
"""backyard.run."""
import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models.base import (
    DBSession,
    Base,
)
from .routes import routes


def main(global_config, **settings):
    """Pyramid WSGI Application."""
    os.environ['CONFIG_FILE'] = global_config.get('__file__')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    routes(config)
    return config.make_wsgi_app()
