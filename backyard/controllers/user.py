# -*- coding: utf-8 -*-
"""backyard.views.user."""
from pyramid.view import view_defaults
from pyramid.response import Response
from ..controller import BaseController
from ..validator import validate_username, validate_password

@view_defaults(route_name='user')
class UserController(BaseController):
    def get(self):
        return Response('get user')
    
    def post(self):
        if self._valid_signup_params():
            resp = Response('register')
        else:
            resp = Response('not valid parameters.')
        return resp

    def delete(self):
        return Response('unregister')

    def _valid_signup_params(self):
        return (validate_username(self.request.params.get('username')) and
                validate_password(self.request.params.get('password'),
                                  self.request.params.get('password_confirmation')))
