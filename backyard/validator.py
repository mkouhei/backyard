# -*- coding: utf-8 -*-
"""backyard.validator."""

def validate_username(username):
    return username != '' # and DBSession.query(User).filter_by(username=username)

def validate_password(password, password_confirmation):
    return password != '' and password == password_confirmation
