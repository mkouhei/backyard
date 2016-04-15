# -*- coding: utf-8 -*-
"""backyard.views.users"""
from pyramid.renderers import get_renderer
from pyramid.view import view_config, notfound_view_config
from backyard.controllers.base import meta


class Views(object):
    """view class."""

    def __init__(self, request):
        """initialize."""
        self.request = request
        renderer = get_renderer('templates/layout.pt')
        self.layout = renderer.implementation().macros['layout']
        self.meta = meta()

    @view_config(route_name='index', renderer='templates/index.pt')
    @view_config(route_name='signup', renderer='templates/signup.pt')
    @view_config(route_name='signin', renderer='templates/signin.pt')
    def index(self):
        """index view."""
        return self.meta

    @notfound_view_config(renderer='templates/error.pt')
    def notfound(self):
        """Not found error page."""
        self.request.response.status = '404 Not Found'
        self.meta['title'] = self.request.response.status
        self.meta['reason'] = "The resource '{0}' could not be found.".format(
            self.request.exception.args[0])
        return self.meta
