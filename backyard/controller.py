# -*- coding: utf-8 -*-
"""backyard.controller."""
import sys
import pkg_resources
from pyramid.renderers import get_renderer, render
from pyramid.view import view_config, notfound_view_config
import backyard

from backyard import (
    __project__,
    __version__,
    __author__,
    __repo__,
    READTHEDOCS
)


def get_ver(pkg_name):
    """package version.

    :rtype: str
    :return: package version

    :param str pkg_name: package name
    """
    return pkg_resources.get_distribution(pkg_name).version


def meta():
    """This project meta data.

    :rtype: dict
    :return: this project meta data
    """
    return dict(project=__project__,
                depver={'python': sys.version.split()[0],
                        'pyramid': get_ver('pyramid')},
                version=__version__,
                author=__author__,
                repo=__repo__,
                docs=READTHEDOCS)


class AbstractController(object):
    def __init__(self, request):
        """initialize."""
        self.request = request
        renderer = get_renderer('views/layout.pt')
        self.layout = renderer.implementation().macros['layout']
        self.meta = meta()


class BaseController(AbstractController):
    """view class."""

    @view_config(route_name='index', renderer='views/index.pt')
    @view_config(route_name='signup', renderer='views/signup.pt')
    @view_config(route_name='login', renderer='views/login.pt')
    def index(self):
        """index view."""
        return self.meta

    @notfound_view_config(renderer='views/error.pt')
    def notfound(self):
        """Not found error page."""
        self.request.response.status = '404 Not Found'
        self.meta['title'] = self.request.response.status
        self.meta['reason'] = "The resource '{0}' could not be found.".format(
            self.request.exception.args[0])
        return self.meta
