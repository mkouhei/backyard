# -*- coding: utf-8 -*-
"""backyard.routes."""

from .controllers.user import UserController
from .controllers.session import SessionController

def routes(config):
    config.add_static_view('assets', 'assets', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')

    config.add_route('user', '/user')
    config.add_view(UserController, attr='get', request_method='GET')
    config.add_view(UserController, attr='post', request_method='POST')
    config.add_view(UserController, attr='delete', request_method='DELETE')

    config.add_route('session', '/user/session')
    config.add_view(SessionController, attr='get', request_method='GET')
    config.add_view(SessionController, attr='post', request_method='POST')
    config.add_view(SessionController, attr='delete', request_method='DELETE')
    config.scan()
