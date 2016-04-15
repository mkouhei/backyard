# -*- coding: utf-8 -*-
"""backyard.run."""
import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models.base import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """Pyramid WSGI Application."""
    os.environ['CONFIG_FILE'] = global_config.get('__file__')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('assets', 'assets', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('signup', '/signup')
    config.add_route('signin', '/signin')
    config.scan()
    return config.make_wsgi_app()
