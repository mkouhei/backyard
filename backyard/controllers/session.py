# -*- coding: utf-8 -*-
"""backyard.views.session."""
from pyramid.view import view_defaults
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from ..controller import BaseController

@view_defaults(route_name='session')
class SessionController(BaseController):
    def get(self):
        return Response('user session')
    
    def post(self):
        if self._authenticate():
            return HTTPFound(location=self.request.route_url('index'))
        else:
            return Response('authentication failure.')

    def delete(self):
        return Response('log out')

    def _authenticate(self):
        print(self.request.authenticated_userid)
        # return authenticate(self.request.params.get('username'),
        #                     self.request.params.get('password'))
        return self.request.params.get('username') != '' and self.request.params.get('password') != ''
